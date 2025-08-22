---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - evm
  - resource-machine
  - protocol-adapter
---

# EVM Protocol Adapter Primitive Interfaces

This section contains descriptions of the implementations of primitive interfaces in the EVM Protocol Adapter.

## Set

The set implementation we use is the [OpenZeppelin `EnumerableSet` v5.2.0](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.2.0/contracts/utils/structs/EnumerableSet.sol) implementation.

## Map

We use two representations of maps.

The first - used in the the core datatype implementation such as the `logicVerifierInputs` - is the representation of a map as a list of structs containing an explicit field for the `key` field, namely `logicVerifierInputs` contains field `Instance` which in turn contains a field `tag` which is seen as a key to the map.

We also use Solidity's `mapping` for the commitment accumilator functionality.

## Fixed Size Type

We used `bytes32` and `uint256` in the implementation.

## Proving System

For the current implementation, for resource logics and the compliance proofs we use the Risc0 proving system, specifically v2.3.1 of Risc0 and the v2.2.2 version of the EVM verifier. The delta values are computed as 2D points (`uint256[2]`) on the `secp256k1` (K-256) elliptic curve and verified using ECDSA.

### Compliance Circuit

Our compliance circuits are fixed size of exactly 2 resources: 1 created and 1 consumed. This allows us to also ensure that the `nonce` of the created resource contains the hash of the consumed resource. This grants uniqueness of comitments automatically given uniqueness of nullifiers.

The compliance verifying key is fixed and hardcoded as:

```solidity
bytes32 internal constant _VERIFYING_KEY = 0xd15203a1b0a6a096d0187241329bed9c8536dd0e61dfe6e348ee5cd10b39cfb4;
```

Other than the checks described in the [[Compliance Proof]] page, the compliance proof for the EVM protocol adapter constraints the created resource to use the nullifier of the consumed resource.

For details, consult the [contrains in the arm-risc0 library](https://github.com/anoma/arm-risc0/blob/73bb97640e24a3533587051fcf58c3ed1a12e8e8/arm/src/compliance.rs#L104).

### Delta Proof

The delta proving system uses the ECDSA signature scheme over the K256 eliptic curve. The signature (delta proof) is the sum of the randomness across all compliance units, while the verification key comes from the keccak-256 hash over the list of all nullifier and commitments pairs obtained by iterating over the compliance units (see [`src/proving/Delta.sol`](https://github.com/anoma/evm-protocol-adapter/blob/6f7cde40aaec5e385408012269b85bb8173a9b87/contracts/src/proving/Delta.sol#L31-L37)). The instance for the proving system comes from the [sum of unit deltas](https://github.com/anoma/evm-protocol-adapter/blob/5fc919dcd3f05edb670fc01aea43d197816e2bbb/contracts/src/ProtocolAdapter.sol#L244), where the latter are generated as the [curve point representation](https://github.com/anoma/arm-risc0/blob/73bb97640e24a3533587051fcf58c3ed1a12e8e8/arm/src/compliance.rs#L174) of corresponding resources.

The [verification](https://github.com/anoma/evm-protocol-adapter/blob/5fc919dcd3f05edb670fc01aea43d197816e2bbb/contracts/src/proving/Delta.sol#L48) tries to recover from the verifying key hash using the proof as the signature and check the correspondence with the instance.

We use [OpenZeppelin's `ECDSA` library](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol) for recovery.

The elliptic curve addition and conversion methods are defined in [`proving/Delta.sol`](https://github.com/anoma/evm-protocol-adapter/blob/6f7cde40aaec5e385408012269b85bb8173a9b87/contracts/src/proving/Delta.sol).
The curve implementation is taken from [Witnet's `eliptic-curve-solidity` library v0.2.1](https://github.com/witnet/elliptic-curve-solidity/tree/0.2.1). This includes:

- [curve parameters](https://github.com/witnet/elliptic-curve-solidity/blob/0.2.1/examples/Secp256k1.sol)
- [curve addition](https://github.com/witnet/elliptic-curve-solidity/blob/3510760b0f20c1156aea795e68b30fe62ce7c20f/contracts/EllipticCurve.sol#L165) (`ecAdd`)
- [curve multiplication](https://github.com/witnet/elliptic-curve-solidity/blob/3510760b0f20c1156aea795e68b30fe62ce7c20f/contracts/EllipticCurve.sol#L239) (`ecMul`)

<!-- We use the zero delta public key derived from the private key `0`. -->

## Commitment Accumilator

Our commitment accumulator is a modified version of OpenZeppelin's [`MerkleTree`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.3.0/contracts/utils/structs/MerkleTree.sol) and [`MerkleProof`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.3.0/contracts/utils/cryptography/MerkleProof.sol) implementations. The core difference is the fact that it is not a constant-sized tree and keep intermediary nodes instead of only leaves in order to support on-chain merkle proof generation.

We only increase the depth whenever we need to. This keeps the gas costs of updating the commitment merkle tree to a minimum. For details, please consult the [documentation](https://github.com/anoma/evm-protocol-adapter/blob/feature/dynamic-cmacc/contracts/src/libs/MerkleTree.sol)).

## Nullifier Accumulator

As our nullifier accumulator we use a set. As noted above, the implementation is provided by [OpenZeppelin `EnumerableSet` v5.2.0](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.2.0/contracts/utils/structs/EnumerableSet.sol) implementation.

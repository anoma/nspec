---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - evm
  - resource-machine
  - protocol-adapter
markdown_extensions:
  - def_list
---

# Execition Flow of the EVM Protocol Adapter

This page tries to go into the high-level detail of the Protocol Adapter implementation on the EVM. This page in particular explains how we address all the out of circuit checks and any additional ones implemented.

## Resource Machine

The resource machine functionality is implemented via the `verify` and `execute` functions.

The `verify` function is a `view` function which implements all the specified resource-machine checks. The `execute` function processes the state change. The execute function updates the commitment accumilator and the nullifier set iff the following criteria get fullfilled:

- `verify` returns true
- All forwarder calls in each `externalPayload` return the expected outcomes (in particular they do not revert)
- Each resource encoded in `appData` connected to an external call actually corresponds to its `tag`

Given all of this is done, all the commitments in a transaction get added to the commitment merkle tree and the nullifiers to the nullifier set. Afterwards, two events ar emitted:

```solidity
event TransactionExecuted(uint256 indexed id, Transaction transaction, bytes32 newRoot);
```

and

```solidity
event ForwarderCallExecuted(address indexed untrustedForwarder, bytes input, bytes output);
```

## User

From the perspective of the user, there are two things they are concerned about:

1) Getting to know which resources are relevant to them
2) Composing and submitting transactions

### Resource State Sync

For the former, the user can listen to the incoming `TransactionExecuted` events and inspect individual `appData` fields. Each user is assumed to have some sets of keypairs. Specifically some sets for decoding the `discoveryPayload` and `resourcePayload` contained in the `appData` of the given `tag`.

While these fields are permissionless, they are incentivized (and frequently required by the resource logics) to contain specific sort of info. Specifically, the user expects that if the `tag` is relevant to them, the `discoveryPayload` decoded to a single byte with their private discovery key. This way the user understands that `tag` is a resource they are interested in. Afterwards, they can use their resource payload decryption key to decrypt `resourcePayload` which they can expect to contain the resource plaintext and other relevant information.

Given the plaintext, the user can then check that the plaintext actually corresponds to the `tag` by committing or nullifying (given that the nullifier key is provided) the resource. That way the user gets to know what resource was created or consumed in a shielded context.

### Transaction Generation

There are only non-application specific pieces of data that a user needs to know regarding the global state if they want to generate a transaction. Both of them are needed to nullify a given resource `R`. These are:

- Some root at which `R` has been created.
- The path to `R` at that root.

If `R` has indeed been created, it exists at the latest root. The EVM PA supports getting the information about the latest root by using the

```solidity
function latestRoot() external view returns (bytes32 root);
```

while getting the merkle proof against the latest state of the tree is achieved by calling

```solidity
function merkleProof(bytes32 commitment) external view returns (bytes32[] memory siblings, uint256 directionBits);
```

Alternative ways of generating proofs against older roots are of course possible but will require third parties generating the historical states of the tree.

## Solvers

Solvers can also get information regarding resources interesting to them similarly to the users: from surveilling the `discoveryPayload`.

## Executor

For the EVM Protocol Adapter the role of the executor depends on the chain on which it has been deployed. For example the executor for the PA deployed on Ethereum the executor will be the validator set of the Ethereum chain.

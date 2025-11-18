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

# Execution Flow of the EVM Protocol Adapter

This page describes at a high-level the Protocol Adapter implementation on the EVM. This page in particular explains how we address all the out of circuit checks and any additional ones implemented.

## Resource Machine

The resource machine functionality is implemented via the `execute` function, processing the verification of the transaction as per the RM specification and updating state consisting of a commitment accumulator, set of historical tree roots, and the nullifier set.

The `execute` function updates the commitment accumulator and the nullifier set if and only if the following two criteria are fulfilled:

- All checks specified by the RM specification pass. In particular:
  + All compliance proofs are valid.
  - All resource logic proofs are valid.
  - The delta proof is valid.
  - For each action, its compliance units partition its tags.
  - Verifying keys of tags match the logic references in the compliance units.
  - Historical roots defined in the compliance units exist in the set of historical roots.
  - There are no repeated commitments or nullifiers in the transaction.
  - Each commitment in a transaction has not been added to the commitment accumulator before.
  - Each nullifier in a transaction has not been added to the nullifier set before.
- All forwarder calls in each `externalPayload` return the expected outcomes and do not revert.

Given all of this is done, all the commitments in a transaction are added to the commitment Merkle tree and the nullifiers are added to the nullifier set. We also emit several events relevant to the transaction during the execution.

Below, we go into details regarding verification and event-emission details.

### Verification

Verification can be split into two conceptual components as specified above:

#### RM Checks

We go through the list explicating how each check is made:

- All compliance proofs are valid.

We grant that by iterating over the compliance units and verifying their proofs by calling the trusted Risc0 Verifier.

- All resource logic proofs are valid.

When iterating over compliance units, for each tag present we fetch the corresponding proofs from the action, verifying it by calling the trusted Risc0 Verifier.

- The delta proof is valid.

At the end of the transaction, we run ECDSA signature verification, which corresponds to verifying a delta proof.

- For each action, its compliance units partition its tags.

This check is split into four components.

1. When iterating over the compliance units of the action, we call `lookup` on every nullifier and commitment. This function iterates over the logic verifier inputs in a given action and reverts if no matching tag has been found. This ensures that the set of tags in compliance unit is a subset of a set of tags of the action.

2. When adding nullifiers to the nullifier set, the operation reverts on a repeating nullifier insertion. This grants that nullifiers across the compliance units are unique.

3. Our compliance circuit ensures that if a resource is committed, it uses a nullifier of a consumed resource present in the same compliance unit as its nonce. Since nullifiers are unique, this statistically grants uniqueness of commitments.

4. During the initial allocation of array sizes for tags, we compute the number of the overall tags by `countTags` function. It in particular ensures that the number of tags in the compliance units and logic verifier inputs match.

- Verifying keys of tags match the logic references in the compliance units.

When doing `lookup` we check that these match explicitly. Note that in this implementation, the hashing function to get the logic reference from the verifying key is just the identity function, hence we check for explicit equality.

- Historical roots defined in the compliance units exist in the set of historical roots.

When iterating over the compliance units, we explicitly check containment of all roots provided in the set of roots we store on-chain.

- There are no repeated commitments or nullifiers in the transaction.

As mentioned, the uniqueness of commitments and nullifiers are granted by the semantics of nullifier set and the compliance circuit constraints.

- Each commitment in a transaction has not been added to the commitment accumulator before.

Same here.

- Each nullifier in a transaction has not been added to the nullifier set before.

Same here.

#### External Call Checks

After verifying a logic proof of a resource, we iterate over the `externalPayload`in its application data. In each position, the verifier expects to be encoded a tuple with:

1. External address
2. Input bytes
3. Output bytes

The external address is assumed to be a forwarder contract which can hence be called via `forwardCall` interface, giving the `logicRef` of the resource and the input bytes as the arguments.

The call ought to return exactly the output bytes, otherwise, the verifier reverts with the appropriate error.


### Events

For each payload blob with deletion criterion `Never`, we emit it as an event to be recorded in Ethereum's history and picked up by apporpriate indexers:

```solidity
event ResourcePayload(bytes32 indexed tag, uint256 index, bytes blob);

event DiscoveryPayload(bytes32 indexed tag, uint256 index, bytes blob);

event ExternalPayload(bytes32 indexed tag, uint256 index, bytes blob);

event ApplicationPayload(bytes32 indexed tag, uint256 index, bytes blob);
```

Regardless of the deletion criterion, we also emit an event signaling that a forwarder call has been made:

```solidity
 event ForwarderCallExecuted(address indexed untrustedForwarder, bytes input, bytes output);
```

Alongside that, we have separate events informing that a specific action has executed with specified root:

```solidity
event ActionExecuted(bytes32 actionTreeRoot, uint256 actionTagCount);
```

And the final transaction event listing all tags and their verification keys in the order provided by the compliance units:

```solidity
event TransactionExecuted(bytes32[] tags, bytes32[] logicRefs);
```


## User

From the perspective of the user, there are two things they are concerned about:

1) Getting to know which resources are relevant to them

2) Composing and submitting transactions

### Resource State Sync

For the former, the user can listen to the incoming `TransactionExecuted` events and inspect individual `appData` fields. Each user is assumed to have some sets of keypairs. Specifically some sets for decoding the `discoveryPayload` and `resourcePayload` contained in the `appData` of the given `tag`.

While these fields are permissionless, they are incentivized (and frequently required by the resource logics) to contain specific sort of info. Specifically, the user expects that if the `tag` is relevant to them, the `discoveryPayload` decodes to a single byte with their private discovery key. This way the user understands that `tag` is a resource they are interested in. Afterwards, they can use their resource payload decryption key to decrypt `resourcePayload` which they can expect to contain the resource plaintext and other relevant information.

If the resource needs to make a forwarder call, the user is expected to put the plaintext in a universally decodable format into the head of the `resourcePayload` alongside with the nullifier key afterwards in the array if the resource making a call is consumed. The PA decided on the validity of the call based on the provided information in these predetermined locations.

Given the plaintext, the user can then check that the plaintext actually corresponds to the `tag` by committing or nullifying (given that the nullifier key is provided) the resource. That way the user gets to know what resource was created or consumed in a shielded context.

### Transaction Generation

There are only two non-application specific pieces of data that a user needs to know regarding the global state if they want to generate a transaction. Both of them are needed to nullify a given resource `R`. These are:

- Some root at which `R` has been created.
- The path to `R` at that root.

If `R` has indeed been created, it exists at the latest root. The EVM PA supports getting the information about the latest root by using the

```solidity
function latestCommitmentTreeRoot() external view returns (bytes32 root);
```

The Merkle proofs are not availiable on-chain for gas reasons.

## Solvers

Solvers can also get information regarding resources interesting to them similarly to the users: from inspecting the `discoveryPayload`.

## Executor

For the EVM Protocol Adapter the role of the executor depends on the chain on which it has been deployed. For example, for the PA deployed on Ethereum the executor will be the validator set of the Ethereum chain.

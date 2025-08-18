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

# EVM Resource Machine Datatypes

This section contains the descriptions of the RM datatype implementations and their interfaces.

The "Proof" sections try to describe the explicit implementation details that may differ from the original RM specification.

## Resource

A [resource](https://github.com/anoma/evm-protocol-adapter/blob/b807463b96c12743e20a07fbafef0b895c1c969f/contracts/src/Types.sol#L16) is implemented as the following Solidity struct:

```solidity
struct Resource {
    bytes32 logicRef;
    bytes32 labelRef;
    bytes32 valueRef;
    bytes32 nullifierKeyCommitment;
    uint256 quantity;
    uint256 nonce;
    uint256 randSeed;
    bool ephemeral;
}
```

### Resource Computable Components

Commitment

:   A commitment of resource `resource` is computed as `sha256(abi.encode(resource))`

Nullifier

:  A nullifier of a resource `resource` with nullifier key `nullifierKey` is computed as `sha256(abi.encode(resource, nullifierKey))`

Kind

:  A kind of a resource `resource` with `logicRef = resource.logicRef` and `labelRef = resource.labelRef` is computed as `sha256(abi.encode(logicRef, labelRef))`.

Delta

:  Given a resource `resource` it's delta gets computed as the multiple of the resource kind and quantity seen as scalars and Pedersen-committed to a 2D point on the K256 curve. However, we do not use them for verification purposes. For details one can consult the [compliance circuit](https://github.com/anoma/arm-risc0/blob/73bb97640e24a3533587051fcf58c3ed1a12e8e8/arm/src/compliance.rs#L170).

## Compliance Unit

The compliance unit is defined as the `VerifierInput` struct:

```solidity
    struct VerifierInput {
        bytes proof;
        Instance instance;
    }
```

whwre the instance is the expected compliance unit instance type:

```solidity
    struct Instance {
        ConsumedRefs consumed;
        CreatedRefs created;
        bytes32 unitDeltaX;
        bytes32 unitDeltaY;
    }
```

where

```solidity
    struct ConsumedRefs {
        bytes32 nullifier;
        bytes32 logicRef;
        bytes32 commitmentTreeRoot;
    }
```

and

```solidity
    struct CreatedRefs {
        bytes32 commitment;
        bytes32 logicRef;
    }
```

As mentioned in [[EVM Primitive Interfaces]] page, the unit delta is represented as a 2D point.

## Action

The action datatype is described as

```solidity
struct Action {
    Logic.VerifierInput[] logicVerifierInputs;
    Compliance.VerifierInput[] complianceVerifierInputs;
}
```

Where the compliance verifier input time is defined above, while the logic verifier input is defined as:

```solidity
    struct VerifierInput {
        bytes proof;
        Instance instance;
        bytes32 verifyingKey;
    }
```

Where the instance is

```solidity
    struct Instance {
        bytes32 tag;
        bool isConsumed;
        bytes32 actionTreeRoot;
        bytes ciphertext;
        Payloads[] appData;
    }
```

The `Payloads` stands for the 4 different payloads we posess:

```solidity
struct Payloads {
    ExpirableBlob[] resourcePayload;
    ExpirableBlob[] discoveryPayload;
    ExpirableBlob[] externalPayload;
    ExpirableBlob[] applicationPayload;
}
```

with `ExpirableBlob` defined as

```solidity
    struct ExpirableBlob {
        DeletionCriterion deletionCriterion;
        bytes blob;
    }
```

There are only two deletion criteria we support:

```solidity
    enum DeletionCriterion {
        Immediately,
        Never
    }
```

The storage of the criteria is designated to the EVM event history logs. Once executed, the event will be transmitted, including the blobs, which will then be recoverable to interested party through Indexing services of their liking.

The `actionTreeRoot` is computed as the root of a merkle tree of depth 4 with leaves provided by the `tag`s in the corresponding Action.

## Transaction

The transaction is defined as a list of actions with some proofs:

```solidity
struct Transaction {
    Action[] actions;
    bytes deltaProof;
}
```

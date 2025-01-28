---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
- ID
- Identity
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.identities;

    import arch.node.types.crypto open public;
    import prelude open;
    ```

# Types for network identities

Types in this section are used to represent identities within the network.

## Basic Types

### Signable

A type representing data that can be cryptographically signed.

```juvix
Signable : Type := ByteString;
```

### Plaintext

Raw unencrypted data.

```juvix
Plaintext : Type := ByteString;
```

### Ciphertext

Encrypted data.

```juvix
Ciphertext : Type := ByteString;
```

### Cryptographic Keys

```juvix
DecryptionKey : Type := ByteString;
SigningKey : Type := ByteString;
```

## Identity Types

### ExternalID

A unique identifier, such as a public key, represented as a natural number.

<!-- --8<-- [start:ExternalID] -->
```juvix
syntax alias ExternalID := PublicKey;
```
<!-- --8<-- [end:ExternalID] -->

### InternalID

A unique identifier, such as a private key, used internally within the network.

```juvix
syntax alias InternalID := PrivateKey;
```

### Identity

A pair combining an `ExternalID` and an `InternalID`.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Commitment

A cryptographic signature or commitment.

```juvix
syntax alias Commitment := Signature;

axiom emptyCommitment : Commitment;
```

## Network Identifiers

### NodeID

Cryptographic node identity.

```juvix
syntax alias NodeID := ExternalID;
```

### TopicID

Cryptographic topic identity.

```juvix
syntax alias TopicID := ExternalID;
```

### PublisherID

Cryptographic identity of a publisher in a pub/sub topic.

```juvix
syntax alias PublisherID := ExternalID;
```

### DomainID

Cryptographic domain identity.

```juvix
syntax alias DomainID := ExternalID;
```

### MemberID

Cryptographic identity of a member in a domain.

```juvix
syntax alias MemberID := ExternalID;
```

### ChunkID

Cryptographic content addressed hash digest of a data chunk.

```juvix
syntax alias ChunkID := Digest;
```

## Engine Related Types

### EngineName

Engine instance name as an opaque string.

```juvix
syntax alias EngineName := String;
```

### ExternalIdentity

An alias for engine name.

```juvix
syntax alias ExternalIdentity := EngineName;
```

### EngineID

Engine instance identity combining node identity and engine name.

<!-- --8<-- [start:EngineID] -->
```juvix
EngineID : Type := Pair (Option NodeID) EngineName;
```
<!-- --8<-- [end:EngineID] -->

```juvix
isLocalEngineID (eid : EngineID) : Bool :=
  case eid of {
    | mkPair none _ := true
    | _ := false
};

isRemoteEngineID (eid : EngineID) : Bool := not (isLocalEngineID eid);
```

### Engine Helper Functions

```juvix
nameGen (str : String) (name : EngineName) (addr : EngineID) : EngineName :=
  name ++str "_" ++str str ++str "_" ++str (snd addr);
```

## Identity Parameters and Capabilities

### IDParams

Supported identity parameter types.
```juvix
type IDParams :=
  | Ed25519
  | Secp256k1
  | BLS;
```

### Backend

Backend connection types.
```juvix
type Backend :=
  | BackendLocalMemory
  | BackendLocalConnection { subtype : String }
  | BackendRemoteConnection { externalIdentity : ExternalIdentity };
```

### Capabilities

Available identity capabilities.
```juvix
type Capabilities :=
  | CapabilityCommit
  | CapabilityDecrypt
  | CapabilityCommitAndDecrypt;
```

## Identity Evidence Types

### IdentityName

Hierarchical identity naming structure.

```juvix
type IdentityName :=
  | LocalName { name : String }
  | DotName { parent : ExternalIdentity; child : String };
```


??? quote "Instances"

    ```juvix
    axiom IdentityNameCmpDummy : IdentityName -> IdentityName -> Ordering;

    instance
    IdentityNameOrd : Ord IdentityName :=
      mkOrd@{
        cmp := IdentityNameCmpDummy;
      };
    ```

### ReadsForEvidence

Evidence of read permissions between identities.

```juvix
type ReadsForEvidence := mkReadsForEvidence {
  fromIdentity : ExternalIdentity;
  toIdentity : ExternalIdentity;
  proof : ByteString;
};
```

??? quote "Instances"

    ```juvix
    axiom ReadsForCmpDummy : ReadsForEvidence -> ReadsForEvidence -> Ordering;

    instance
    ReadsForOrd : Ord ReadsForEvidence :=
    mkOrd@{
      cmp := ReadsForCmpDummy;
    };
    ```

### SignsForEvidence

Evidence of signing permissions between identities.

```juvix
type SignsForEvidence := mkSignsForEvidence {
  fromIdentity : ExternalIdentity;
  toIdentity : ExternalIdentity;
  proof : ByteString;
};
```

??? quote "Instances"

    ```juvix
    axiom SignsForCmpDummy : SignsForEvidence -> SignsForEvidence -> Ordering;

    instance
    SignsForOrd : Ord SignsForEvidence :=
      mkOrd@{
    cmp := SignsForCmpDummy;
    };
    ```

### IdentityNameEvidence

Evidence linking identity names to external identities.

```juvix
type IdentityNameEvidence := mkIdentityNameEvidence {
  identityName : IdentityName;
  externalIdentity : ExternalIdentity;
  proof : ByteString;
};
```

??? quote "Instances"

    ```juvix
    axiom IdentityNameEvidenceCmpDummy : IdentityNameEvidence ->
      IdentityNameEvidence -> Ordering;

    instance
    IdentityNameEvidenceOrd : Ord IdentityNameEvidence :=
      mkOrd@{
        cmp := IdentityNameEvidenceCmpDummy;
      };
    ```

### Ordering Aliases

```juvix
type TransactionLabel ReadLabel WriteLabel := mkTransactionLabel {
  read : List ReadLabel;
  write : List WriteLabel
};
syntax alias TxFingerprint := Nat;
type TransactionCandidate ReadLabel WriteLabel Executable := mkTransactionCandidate {
  label : TransactionLabel ReadLabel WriteLabel;
  executable : Executable
};
syntax alias NarwhalBlock := String;
syntax alias BatchNumber := Nat;
syntax alias WallClockTime := Nat;
```

Don't know a better place to put this.
```juvix
-- Map a key to its shard
axiom keyToShard {KVSKey} : KVSKey -> EngineID;
```

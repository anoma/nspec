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
    module node_architecture.types.identities;
    import Stdlib.Data.String.Base open;
    import Stdlib.Trait.Ord open using {Ordering; Ord; mkOrd};
    import node_architecture.types.crypto open;
    import prelude open;
    ```

# Types for network identities

Types in this section are used to represent identities within the network.

## Basic Types

### ByteString

A basic type for representing binary data.

```juvix
ByteString : Type := Nat;

emptyByteString : ByteString := 0;
```

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

```juvix
syntax alias ExternalID := PublicKey;
```

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

### DomainID

Cryptographic domain identity.

```juvix
syntax alias DomainID := ExternalID;
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

```juvix
EngineID : Type := Pair (Option NodeID) (Option EngineName);

unknownEngineID : EngineID := mkPair none none;

isLocalEngineID (eid : EngineID) : Bool :=
  case eid of {
    | mkPair none _ := true
    | _ := false
};

isRemoteEngineID (eid : EngineID) : Bool := not (isLocalEngineID eid);
```

### Engine Helper Functions

```juvix
nameStr (name : EngineID) : String :=
  case snd name of {
    | none := ""
    | some s := s
  };

nameGen (str : String) (name : EngineName) (addr : EngineID) : EngineName :=
  (name ++str "_" ++str str ++str "_" ++str nameStr addr);
```

## String Comparison
```juvix
axiom stringCmp : String -> String -> Ordering;

instance
StringOrd : Ord String :=
  mkOrd@{
    cmp := stringCmp;
  };
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
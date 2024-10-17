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

??? note "Juvix imports"

    ```juvix
    module node_architecture.types.identities;
    import node_architecture.types.crypto open;
    import prelude open;
    ```

## Types for network identities

Types in this section are used to represent [[Identity|identities]] within the network.

### ExternalID

A unique identifier, such as a public key, represented as a natural number.

```juvix
syntax alias ExternalID := PublicKey;
```

### InternalID

A unique identifier, such as a private key, used internally within the network,
represented as a natural number.

```juvix
syntax alias InternalID := PrivateKey;
```

### Identity

A pair combining an `ExternalID` and an `InternalID`, representing the complete
identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Commitment

A cryptographic signature, or commitment.
Signed by an internal identity and verifiable by an external identity.

```juvix
syntax alias Commitment := Signature;
```

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

### EngineName

Engine instance name.
An opaque string that is unique to the local node.

```juvix
syntax alias EngineName := String;
```

### EngineID

Engine instance identity. A pair of an optional node identity (when remote) and
an engine instance name (which may not be present, stands for anonymous engine).

!!! info

    We assume that the engine instance name is unique within the node.

```juvix
EngineID : Type := Pair (Option NodeID) (Option EngineName);
```

```juvix
unknownEngineID : EngineID := mkPair none none;
```

```juvix
isLocalEngineID (eid : EngineID) : Bool :=
  case eid of {
    | mkPair none _ := true
    | _ := false
};
```

```juvix
isRemoteEngineID (eid : EngineID) : Bool := not (isLocalEngineID eid);
```

```juvix
ByteString : Type := Nat;
emptyByteString : ByteString := 0;
Signable : Type := ByteString;
axiom emptyCommitment : Commitment;
DecryptionKey : Type := ByteString;
SigningKey : Type := ByteString;
Plaintext : Type := ByteString;
Ciphertext : Type := ByteString;

syntax alias ExternalIdentity := EngineName;
```
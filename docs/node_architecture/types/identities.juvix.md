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

Engine instance identity.
A pair of an engine instance name and an optional node identity (when remote).

```juvix
EngineID : Type := Pair (Maybe NodeID) EngineName;
```

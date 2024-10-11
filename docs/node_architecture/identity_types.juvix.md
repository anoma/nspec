---
icon: octicons/container-24
search:
  exclude: false
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.identity_types;

    import prelude open;
    ```

## Types for network identities

Types in this section are used to represent [[Identity|identities]] within the network.

### ExternalID

A unique identifier, such as a public key, represented as a natural number.

```juvix
syntax alias ExternalID := Nat;
```

### InternalID

A unique identifier, such as a private key, used internally within the network,
represented as a natural number.

```juvix
syntax alias InternalID := Nat;
```

### Identity

A pair combining an `ExternalID` and an `InternalID`, representing the complete
identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Commitment

A cryptographic signature, or commitment,
signed by an internal identity and verifiable by an external identity.

```juvix
syntax alias Commitment := Nat;
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
An engine instance name and an optional node identity (for engines on remote nodes).

```juvix
EngineID : Type := Pair (Maybe NodeID) EngineName;
```

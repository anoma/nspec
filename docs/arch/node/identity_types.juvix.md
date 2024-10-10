---
icon: octicons/container-24
search:
  exclude: false
---

??? note "Juvix imports"

    ```juvix
    module arch.node.identity_types;

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

### Name

A name could be a simple string without any particular meaning in the system or
an external identity.

```juvix
Name : Type := Either String ExternalID;
```

### Address

An address is a name used for forwarding messages to the correct destination.

```juvix
syntax alias Address := Name;
```

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
---

??? info "Juvix imports"

    ```juvix
    module node_architecture.basics;
    import prelude open public;
    import prelude open using {Hash} public;
    ```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node
architecture prelude. For a more general prelude, please refer to
[Juvix Base Prelude](./../prelude.juvix.md). (1)
{ .annotate }

1. :woman_raising_hand: If you are unfamiliar with Juvix,
please refer to the [Juvix documentation](https://docs.juvix.org/latest/tutorials/learn.html).

## Types for network identities

<!-- This section needs to be reworked. -->

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

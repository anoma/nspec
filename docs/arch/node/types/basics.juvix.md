---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.basics;
    import prelude open public;
    ```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node
architecture prelude. For a more general prelude, please refer to
[[Juvix Base Prelude]]. (1)
{ .annotate }

1. :woman_raising_hand: If you are unfamiliar with Juvix,
please refer to the [Juvix documentation](https://docs.juvix.org/latest/tutorials/learn.html).

## Basic types

### Bytes

Byte array.

```juvix
syntax alias Bytes := String;
```

### Hash

Natural numbers are used (for now) to represent hash values, bytes sizes, and other non-negative integers.

```juvix
syntax alias Hash := Nat;
```

### RelTime

Relative time.
In seconds from now.

```juvix
syntax alias RelTime := Nat;
```

### AbsTime

Absolute time.
In minutes since epoch (2024-01-01 00:00).

```juvix
syntax alias AbsTime := Nat;
```

### Time

Either absolute or relative time.

```juvix
Time : Type := Either RelTime AbsTime;
```

### Version

Semantic version number (major.minor.patch).

```juvix
type Version : Type :=
  mkVersion {
    major : Nat;
    minor : Nat;
    patch : Nat;
  };
```

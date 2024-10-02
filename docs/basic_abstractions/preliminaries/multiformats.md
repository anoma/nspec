---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Multiformats

A _multiformat_ (directly inspired by the [concept of the same name by Protocol
Labs](https://multiformats.io/)) is an interface consisting of typed functions
associated with a table of multiple implementations of that interface, each
associated with a unique natural number (non-negative integer), such that the
numerical code can be included to indicate which implementation should be used
to interpret/process some data. Conceptually, multiformats can also be
understood as an implementation of runtime-updateable typeclasses (in the
Haskell sense), where new instances can be added associated with new codes.

An example table for an encoding scheme multiformat could look like:

| Code | Encoding scheme |
| - | - |
| 0x01 | [SSZ](https://github.com/ethereum/consensus-specs/blob/dev/ssz/simple-serialize.md) |
| 0x02 | JSON |
| 0x03 | [Borsh](https://borsh.io/) |
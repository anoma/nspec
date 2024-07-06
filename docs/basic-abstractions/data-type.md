---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Data type

The protocol standardises basic types and general algebraic data types. Standardisation of data types allows for interoperability between different encoding schemes and virtual machines.

All messages sent and received within and between nodes and all parts of state must have an associated data type. Data types used by the protocol itself are fixed a priori (by this specification). Data types used by applications are chosen by application authors, serialised, and passed around at runtime in order to handle data appropriately.

A _basic type_ is defined as either:

- a boolean value (bit)
- a ring $Z_n$ of natural numbers $\mathrm{mod}~n$
- a finite field $\mathbb{F}_n$ of order $n$
- a bytestring (binary data of unbounded length)

```juvix
type BasicType :=
  | Boolean
  | Ring Nat
  | FiniteField Nat
  | Bytestring
```

A _data type_ is defined as either:

- a basic type
- a product of other data types
- a coproduct of other data types
- a function type from one data type to another data type

```juvix
type DataType :=
  | Basic BasicType
  | Product [DataType]
  | Coproduct [DataType]
  | Function A B
```

<!--
Open questions:
- Can function types be included in / mutually recursive with data types like this?
- Alternatively, we could split function types into a separate thing, but this is less flexible.
- "multiencode" / "multidecode" functions which take:
  - in case of encoding, preferences about how to encode data and how to encode functions
  - in case of decoding, the multiformats (both virtual machine + encoding scheme)
  - ... and behave appropriately. decoding will fail if unknown multiformats are encountered
-->
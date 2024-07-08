---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Data type

The protocol standardises basic types and general algebraic data types. Standardisation of data types allows for interoperability between different encoding schemes and virtual machines.

All messages sent and received within and between nodes and all parts of state must have an associated data type. Data types used by the protocol itself are fixed a priori (by this specification). Implementation languges will typically represent these types as native types in their typesystem, such that the implementation language can provide typechecking. Data types used by applications are chosen by application authors, serialised, and passed around at runtime in order to handle data appropriately.

## Types

A _basic type_ is defined as either:

- a boolean (bit) type
- a ring type $Z_n$ of natural numbers $\mathrm{mod}~n$
- a finite field type $\mathbb{F}_n$ of order $n$
- a bytestring (binary data of unbounded length) type

```juvix
type BasicType :=
  | BooleanT
  | RingT Nat
  | FiniteFieldT Nat
  | BytestringT
```

A _data type_ is defined as either:

- a basic type
- a product of other data types
- a coproduct of other data types
- a function type from one data type to another data type

```juvix
type DataType :=
  | BasicT BasicType
  | ProductT [DataType]
  | CoproductT [DataType]
  | FunctionT A B
```

## Values

A _basic value_ is defined as either:

- a boolean value
- a ring value $n$ (between $0$ and $n-1$)
- a finite field value $\mathbb{F}_n$ (a natural number $n$ represents the $n$th element of the finite field)
- a bytestring (binary data of unbounded length) type

```juvix
type BasicValue :=
  | BooleanV Boolean
  | RingV Nat
  | FiniteFieldV Nat
  | BytestringV Bytestring
```

A _data value_ is defined as either:

- a basic value
- a tuple of other data values (inhabitant of a product type)
- a option with an index and a data value (inhabitant of a coproduct type)
- a function value (represented with a particular virtual machine)

```juvix
type DataValue :=
  | BasicV BasicValue
  | TupleV [DataValue]
  | OptionV Nat DataValue
  | FunctionV Nat Bytestring
```

<!--
Should FunctionV be a Repr type?
-->

## Typechecking

The obvious typechecking relation

```juvix
typecheck : DataValue -> DataType -> Boolean
```

can be implemented.

<!--
Open questions:
- Can function types be included in / mutually recursive with data types like this?
- Alternatively, we could split function types into a separate thing, but this is less flexible.
- "multiencode" / "multidecode" functions which take:
  - in case of encoding, preferences about how to encode data and how to encode functions
  - in case of decoding, the multiformats (both virtual machine + encoding scheme)
  - ... and behave appropriately. decoding will fail if unknown multiformats are encountered
-->
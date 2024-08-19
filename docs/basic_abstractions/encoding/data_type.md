---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Data type

The protocol standardises basic types and general algebraic data types. All messages sent and received within and between nodes and all parts of state must have an associated data type. Data types used by the protocol itself are fixed a priori (by this specification). Implementation languges will typically represent these types as native types in their typesystem, such that the implementation language can provide typechecking. Data types used by applications are chosen by application authors, serialised, and passed around at runtime in order to handle data appropriately.

## Types

### Basic types

A _basic type_ is defined as either:

- a boolean (bit) type
- a ring type $Z_n$ of natural numbers $\mathrm{mod}~n$
- a finite field type $\mathbb{F}_n$ of order $n$
- a natural number type $\mathbb{N}$ (an arbitrary natural number)
- a bytestring (binary data of unbounded length) type

```juvix
type BasicType :=
  | BooleanT
  | RingT Nat
  | FiniteFieldT Nat
  | NatT
  | BytestringT
```

### Data types

A _data type_ is defined as either:

- a basic type
- a product of other data types
- a coproduct of other data types
- a function type from one data type to another data type

!!! note

    Here `[]` is used as shorthand notation for an ordered list of at least one element.

```juvix
type DataType :=
  | BasicT BasicType
  | ProductT [DataType]
  | CoproductT [DataType]
  | FunctionT DataType DataType
```

## Values

### Basic values

A _basic value_ is defined as either:

- a boolean value
- a ring value $n$ (between $0$ and $n-1$)
- a finite field value $\mathbb{F}_n$ (a natural number $n$ represents the $n$th element of the finite field)
- a natural number value
- a binary (binary data of unbounded length) type
- a function value (represented with a particular virtual machine, identified by a natural number)

```juvix
type BasicValue :=
  | BooleanV Boolean
  | RingV Nat
  | FiniteFieldV Nat
  | NatV Nat
  | BinaryV Bytestring
  | FunctionV Nat Bytestring
```

### Data values

A _data value_ is defined as either:

- a basic value
- a tuple of other data values (inhabitant of a product type)
- a option with an index and a data value (inhabitant of a coproduct type)

```juvix
type DataValue :=
  | BasicV BasicValue
  | TupleV [DataValue]
  | OptionV Nat DataValue
```

## Typechecking

The typechecking relation

```juvix
typecheck : DataValue -> DataType -> Boolean
```

can be implemented in the obvious manner. Typechecking functions would require typechecking support from particular virtual machines, which isn’t covered for now, but could be added in the future in a straightforward way.
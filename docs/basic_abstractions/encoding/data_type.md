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

- a finite set type, of order $n$
- a natural number type (arbitrary-size)
- a function type from one data type to another data type

```juvix
type BasicType :=
  | FinSetT Nat
  | NatT
  | FunctionT DataType DataType
```

!!! note

    This set of basic types is minimal, designed only to distinguish between fixed-size values, variable-size values, and functions. Other semantic information (e.g. whether a finite set value is intended to represent a ring or a finite field) will be tracked at a separate layer.

### Data types

A _data type_ is defined as either:

- a basic type
- a product of other data types
- a coproduct of other data types

!!! note

    Here `[]` is used as shorthand notation for an ordered list of at least one element.

!!! note

    Here `[]` is used as shorthand notation for an ordered list of at least one element.

```juvix
type DataType :=
  | BasicT BasicType
  | ProductT [DataType]
  | CoproductT [DataType]
```

## Values

### Basic values

A _basic value_ is defined as either:

- a natural number value $n$
- a function value (represented with a particular virtual machine, identified by a natural number)

```juvix
type BasicValue :=
  | NatV Nat
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
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---


# Encoding scheme

An _encoding scheme_ is a bijective mapping between structured data and a series of bytes, uniquely defined by the pair of serialization and deserialization functions.

## Serialization

The _serialize_ function serializes a data value into a bytestring.

```
type Serialize = DataValue -> Bytes
```

## Deserialization

The _deserialize_ function attempts to deserialize a bytestring into a data value of the specified type.

```juvix
type Deserialize = DataType -> Bytestring -> Maybe DataValue
```

### Properties

These functions must be inverses of each other, in that:

- deserializing a serialized value will result in `Just <that value>`
- serializing a deserialized value will result in the same bytestring

Furthermore, the mapping - given a type - must be bijective: fixing a given type, no two distinct bytestrings can deserialise into the same value, and no two distinct values can serialise into the same bytestring. A bijective mapping without fixing a type can be achieved simply by also serialising the type.

## Multiformat

The protocol standardizes a table of encoding schemes, where each encoding scheme is associated with a unique natural number.

Nodes running the protocol then associate each number with a pair of _serialialize_ and _deserialize_ functions. In order to interoperate correctly, nodes must agree on which number is associated with which encoding scheme, so this table is part of the definition of any particular protocol version, and new entries to the table, once added, cannot be changed. In general, adding new entries to the table should not break anything - a node encountering an encoding scheme it does not know simply fails.

The concrete table is provided in the [Implementation](../../implementation/index.md) section of the specs.
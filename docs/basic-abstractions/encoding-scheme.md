---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Encoding scheme

An _encoding scheme_ is a function which maps between structured data and a series of bytes, uniquely defined by the pair of serialisation and deserialisation functions.

## Serialisation

The `serialise` function serialises a data value into a bytestring.

```
type Serialise = Value -> Bytes
```

## Deserialisation

The `deserialise` function attempts to deserialise a bytestring into a data value of the specified type.

```juvix
type Deserialise = Datatype -> Bytestring -> Maybe Value
```

These functions must be inverses, i.e.:

- `deserialise . serialise = id`
- `serialise . deserialise = id`
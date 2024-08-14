---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Multiencoding

The _multiencode_ function takes a value in internal representation and a set of preferences, and tries to encode it in a bytestring according to those preferences. To convert between virtual machine representations, this will require compilation (which will not be supported in all cases). Multiformat codes will be included to indicate which formats are in use.

```juvix
multiencode : Preferences -> DataValue -> Bytestring
```

The _multidecode_ function takes a value in bytestring representation and tries to decode it into an internal representation, according to the multiformat information and the data encoding and virtual machine formats known by the decoding party. Attempting to decode unknown formats will result in an error.

```juvix
multidecode : Bytestring -> DataType -> ...
```

In general, canonical commitments to data and code are made over the output of _multiencode_. Multiencoding is also used before storing data or sending it over the network. Any party should be able to take any piece of stored or sent data and a type and attempt to deserialise it with _multidecode_.
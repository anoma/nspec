---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# SSZ

The SimpleSerialize (SSZ) format is defined by Ethereum 2 [here](https://github.com/ethereum/consensus-specs/blob/dev/ssz/simple-serialize.md).

SSZ defines encoding, decoding, Merkleization, Merkle multiproofs, and a canonical JSON mapping for the `SSZObject` type

```juvix
type SSZBasicType :=
  uint8 |
  uint16 |
  uint32 |
  uint64 |
  uint128 |
  uint256 |
  byte |
  boolean

type SSZObjectType :=
  Container [(String, SSZObjectType)] |
  Vector SSZObjectType Natural |
  List SSZObjectType Natural |
  Bitvector Natural |
  Bitlist Natural |
  Union [SSZObjectType]
```

We thus define functions to map between general algebraic data types and `SSZObject`:

!!! todo

    Define functions to map between general algebraic data types and SSZObject.
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Data encoding

Data is encoded as the pair of a natural number identifier (specifying a particular encoding format) and a bytestring (to be interpreted by the encoding format):

```juvix
type Data = mkData {
  formatIdentifier : Natural;
  formatBytestring : []byte;
}
```

| Identifier | Encoding format |
| - | - | 
| 0x00 | - (reserved for the future) |
| 0x01 | - (reserved for the future) |
| 0x02 | [SSZ](./ssz.md) |

We then define the canonical data encoding functions as a switch-case over these particular schemes.
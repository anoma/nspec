---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Hash encoding

Hashes are encoded as the pair of a natural number identifier (specifying a particular hash function) and bytes (the output of the hash function).

```juvix
type Hash := mkHash {
    hashIdentifier : Natural;
    hashBytes : []byte;
};
```

| Identifier | Hash function |
| - | - | 
| 0x00 | - (reserved for the future) |
| 0x01 | - (reserved for the future) |
| 0x02 | [SHA3](./sha3.md)

We then define the canonical hash function as a switch-case over these particular virtual machines.
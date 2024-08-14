# Proof encoding

Proof are encoded as the pair of a natural number identifier (specifying a particular proof system) and bytes (the proof content).

```juvix
type Proof := mkProof {
    proofSystemIdentifier : Natural;
    proofSystemBytes : []byte;
};
```

| Identifier | Hash function |
| - | - | 
| 0x00 | - (reserved for the future) |
| 0x01 | - (reserved for the future) |

We then define the canonical proof verifier as a switch-case over these proving systems.
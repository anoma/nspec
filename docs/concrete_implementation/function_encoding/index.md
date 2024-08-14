---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Function encoding

Functions are encoded as the pair of a natural number identifier (specifying a particular virtual machine) and bytecode (to be interpreted by the virtual machine):

```juvix
type Function := mkFunction {
    vmIdentifier : Natural;
    vmBytecode : []byte;
};
```

| Identifier | Virtual machine |
| - | - | 
| 0x00 | - (reserved for the future) |
| 0x01 | - (reserved for the future) |
| 0x02 | [Nockma](./nockma.md) |
| 0x03 | [Cairo](./cairo.md) |
| 0x04 | [RISC0](./risc0.md) |

We then define the canonical function encoding functions as a switch-case over these particular virtual machines.
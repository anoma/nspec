# Global state

The global replicated state includes the commitment accumulator that contains commitments of all created resources and a nullifier set that contains nullifiers of all consumed resources. The commitment tree is currently instantiated as a Merkle tree of variable depth.

## Commitment tree parameters

|Parameter|Instantiation|
|-|-|
|Intermediate node|`SHA256`|
|Leaf|`SHA256` (resource commitment)|
|Depth|Variable|

##### Variable depth Merkle tree

RISC Zero zkVM allows to pass arguments of variable size (vectors) as private or public input to the circuit without changing the proving and verifying keys of the circuit. Changing proving and verifying keys of circuits is equivalent to changing the circuit and is undesirable (unless there is a good reason for it).

Therefore, this feature of RISC Zero zkVM is particularly useful for passing Merkle paths of variable length to the circuits. It allows having Merkle trees of variable size, which can be helpful to decrease the cost of the computation (the tree size is minimal necessary to accommodate the elements stored) and, in principle, to grow unbounded.

We also utilise this feature to have variable depth [action trees](./action.md).

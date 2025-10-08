# Merkle tree

We use SHA256 to compute the hashes in the tree. The tree size is not fixed.
##### Variable size

RISC Zero zkVM allows to pass arguments of variable size (vectors) as private or public input to the circuit without changing the verifying key of the circuit. This is particularly useful for passing Merkle paths to the circuits, as it allows us to have Merkle trees of variable size: the path length depends on the tree depth. Having Merkle trees of variable size allows to decrease the cost of the computation (the tree size is minimal necessary to accommodate the elements stored) and, in principle, to grow unbounded.

This feature allows us to have:
- variable depth commitment tree. Variable depth commitment tree implies variable size inclusion proof, which is used in the compliance circuit to prove the existence of a resource.
- variable size action trees. Action trees are used to pass all resource tags from the action to the logic.

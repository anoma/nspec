---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction function format
The system used to represent and interpret transaction functions must have a deterministic computation model; each operation should have a fixed cost of space and time (for total cost computation). To support content addressing, it must have memory and support memory operations (specifically `read`, `write`, `allocate`).

The system must support the following I/O operations:

1. `readStorage`(`address`: `Commitment`): read the global content-addressed storage at the specified address and return the value stored at the address. If the value is not found, the operation should return an error. Storage not accessible to the machine should be treated as non-existent.
2. `dataByIndex`(`indexFunction)`: read data from the storage (either resources or arbitrary data kept in the storage requested by the transaction function) at the execution time by the specified index function. If the index function output is invalid or uncomputable, or the data cannot be located, the operation should return an error. Typically, the index functions allowed will be very restricted, e.g. an index function returning current unspent resources of a particular kind.


## Gas model
To compute and bound the total cost of computation, the transaction function system must support a gas model. Each evaluation would have a gas limit $g_{limit}$, and the evaluation would start with $g_{count} = 0$. Evaluating an operation, the system would add the cost of the operation to the counter $g_{count}$ and compare it to $g_{limit}$. When making recursive calls, $g_{count}$ is incremented before the recursion occurs. If the value of $g_{count}$ is greater than $g_{limit}$, the execution is terminated with an error message indicating that the gas limit has been surpassed.

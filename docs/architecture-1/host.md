# Host model


Host machines must possess:
- Classical computation (Turing machine)
- The ability to send and receive messages on any number of physical network interfaces
- Local randomness generation
- For user input and control, a trusted user interface

## Computational model


Fix a finite set of finite fields $F_{i}$ ($i$ is the index).

This set must include the two-element binary field $F_b$ and a designated hash field $F_h$.

Each field $F_i$ provides the following primitive operations:

- Multiplication: $*_{F_i}$, with type $F_i \to F_i \to F_i$
- Addition: $+_{F_i}$, with type $F_i \to F_i \to F_i$
- Additive identity: $0_{F_i}$, with type $F_i$
- Multiplicative identity: $1_{F_i}$, with type $F_i$
- Additive inverse: $-_{F_i}$, with type $F_i \to F_i$
- Multiplicative inverse: $1/_{F_i}$, with type $F_i \to F_i$
- Equality: $=_{F_i}$, with type $F_i \to F_i \to {0_{F_b} | 1_{F_b}}$

Each field $F_i$ has order ${F_{i_{order}}}$.

Additionally, we assume a field conversion function for each unique pair $F_i, F_j$ with $i \neq j$:

- Conversion: $conv_{i, j}$
    - With type $F_i \to F_j$ if $F_{i_{order}} \leq F_{j_{order}}$, where no overflow is possible.
    - With type $F_i \to (F_j, F_b)$ if $F_{i_{order}} > F_{j_{order}}$, where the bit $F_b$ in the return value indicates whether the conversion overflowed.

The designated hash function $H$ maps arbitrary lists of $F_i$ to the designated hash field $F_h$.

## Computational costs


We assume bounded, known costs in energy and local (clock) time for all finite field operations defined above.

## Memory costs


We assume a boundable, known, monotonically increasing cost of nonlocality of reference ([ref](https://en.wikipedia.org/wiki/Locality_of_reference)).

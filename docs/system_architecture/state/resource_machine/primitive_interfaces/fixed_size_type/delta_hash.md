# Delta hash

Delta hash is a unique interface that implements both Hash type and Arithmetic type. It is also required to be additively homomorphic and kind-distinct:

- For resources of the same kind $kind$, $h_{\Delta}$ should be *additively homomorphic*:
$\Delta_1 + \Delta_2 = h_{\Delta}(kind, q_1) + h_{\Delta}(kind, q_2) = h_{\Delta}(kind, q_1 + q_2)$
- For resources of different kinds, $h_\Delta$ has to be computationally *kind-distinct*: if there exists $kind$ and $q$ s.t. $h_\Delta(kind_1, q_1) + h_\Delta(kind_2, q_2) = h_\Delta(kind, q)$, it is computationally infeasible to compute $kind$ and $q$.

> An example of a function that satisfies these properties is the Pedersen commitment scheme: it is additively homomorphic, and its kind-distinctness property comes from the discrete logarithm assumption.
# Delta hash

Delta hash is an interface that implements both `Hash` type and `Arithmetic` type. It is also required to be additively homomorphic and kind-distinct:

1. For resources of the same kind $kind$, $h_{\Delta}$ should be *additively homomorphic*:
$\Delta_1 + \Delta_2 = h_{\Delta}(kind, q_1) + h_{\Delta}(kind, q_2) = h_{\Delta}(kind, q_1 + q_2)$
2. For resources of different kinds, $h_\Delta$ has to be computationally *kind-distinct*: if there exists $kind$ and $q$ s.t. $h_\Delta(kind_1, q_1) + h_\Delta(kind_2, q_2) = h_\Delta(kind, q)$, it is computationally infeasible to compute $kind$ and $q$.

!!! note
    An example of a function that satisfies these properties is the [Pedersen commitment scheme](https://link.springer.com/content/pdf/10.1007/3-540-46766-1_9.pdf#page=3): it is additively homomorphic, and its kind-distinctness property comes from the discrete logarithm assumption.

# Used in
1. Resource delta
2. Compliance unit delta
3. Action delta
4. Transaction delta

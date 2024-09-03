---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Delta
Resource deltas are used to reason about the total quantities of different kinds of resources in transactions. For a resource $r$, its delta is computed as $r.\Delta = h_{\Delta}(r.kind, r.q)$.

The function used to derive $r.\Delta$ must have the following properties:

- For resources of the same kind $kind$, $h_{\Delta}$ should be *additively homomorphic*:
$r_1.\Delta + r_2.\Delta = h_{\Delta}(kind, r_1.q + r_2.q)$
- For resources of different kinds, $h_\Delta$ has to be *kind-distinct*: if there exists $kind$ and $q$ s.t. $h_\Delta(r_1.kind, r_1.q) + h_\Delta(r_2.kind, r_2.q) = h_\Delta(kind, q)$, it is computationally infeasible to compute $kind$ and $q$.


> An example of a function that satisfies these properties is the Pedersen commitment scheme: it is additively homomorphic, and its kind-distinctness property comes from the discrete logarithm assumption.

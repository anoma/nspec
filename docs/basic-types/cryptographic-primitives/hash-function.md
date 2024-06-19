---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Hash function

For a function $h$, we denote the output finite field of $h$ as $\mathbb{F}_h$. If a function $h$ is used to derive a component $x$, we refer to the function as $h_x$, and the corresponding to $h$ finite field is denoted as $\mathbb{F}_{h_x}$, or, for simplicity, $\mathbb{F}_x$.

$h$ must be:

- one-way, in that it is not computationally feasible for any agent to compute the preimage from the hash output
- collision-resistant, in that it is not computationally feasible for any agent to find two different preimages which hash to the same value
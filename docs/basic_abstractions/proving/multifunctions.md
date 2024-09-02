---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Multifunctions

## Proof-aware multievaluation

We can define a version of multievaluate which is "proof-aware", in that, each evaluation step, `multievaluate` can also search through known assumptions and proofs, and use them if applicable to replace the term being evaluated (or parts of the term being evaluated) with other terms known to be equal given the known proofs and selected assumptions.

!!! todo

    There are some efficiency questions to reason through here - obviously searching for all possible simplifications each step is not going to be performant - we may need to pass hints somehow of when simplification should be attempted.
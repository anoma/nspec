---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Assumption

What is an assumption? Operationally speaking, the protocol characterizes
assumptions as beliefs about logical impliciations ($a \implies b$ for some $a$
and some $b$); for example:

- $a$ could be that a particular trusted party has signed over a statement, and $b$ could be that the statement is 

- $a$ could be nothing, and $b$ could be that [the algebraic group model
  holds](https://eprint.iacr.org/2017/620.pdf) (this assumption is often relied
  upon by cryptographic proof systems)

- $a$ could be nothing, and $b$ could be that $c = c$ (the identity case)

In an ideal world, the protocol could characterize all of these assumptions
exactly (e.g. as mathematical statements) - however, that will not be feasible
in the short term (precisely expressing cryptographic assumptions will require a
sophisticated specification language), so for now the protocol standardizes an
extensible sum type that can evolve along with the `Proof` multiformat (to add
new types of assumptions).

!!! note

    The encoding here needs to allow for additions to the sum type without breaking backwards compatibility (which may be a property we often want in general).

## Data structure

```
type Assumption :=
  | HashRandomOracle
  | FullyTrust ExternalIdentity
```
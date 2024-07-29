---
icon: material/pillar
search:
  exclude: false
  boost: 2
---

# Introduction


_"There are two kinds of data structures: DAGs, and bad data structures." - unknown_


Anoma's protocol layers themselves form an information-theoretic DAG, in that
higher layers can depend on information from lower layers, but not vice-versa
--lower layers are blind to the syntax and semantics of higher layers, and data of
concern to higher layers is represented in lower layers as opaque bytestrings.
This rule, however, is partially broken in one place-- an identity can be
defined in such a way that it evolves in logical time, and thus depends on a
particular view of a logical DAG --but there is still a DAG in time, the cycle
is only in this document.

The protocol architecture described herein makes no decisions --it is
completely constrained by the context and desiderata heretofore enumerated, and
modulo the two unique up to isomorphism. The protocol is not general for
generality's sake, but rather because only a correct disentanglement of
abstractions and relations can provide the requisite theoretical basis for
understanding what it is exactly that the system does and ensure complete
deduplication of engineering efforts.

!!! todo

    Question: "Prove this (unique up to isomorphism)" If it doesn't hold we've
    probably described something slightly incorrectly.

Parameters are external input to the system, or derived from the combination of
external inputs to the system over time, and since external inputs may depend on
the state of the system, which is accessible to agents choosing those inputs, as
intermediated by the agents making choices the gestalt forms a feedback
mechanism.



!!! note

    Although this document does not use the language or process and cannot claim a similar depth of expertise, we have taken some inspiration from Conal Elliot's [denotational design](https://www.typetheoryforall.com/2022/08/04/21-Conal-Eliott-2.html).


We first describe on the highest level of abstraction what it means to be a
correct implementation of Anoma and how it is structured. This already involves
some design choices and assumptions, like identifying the participating
entities, their actions, and the hardware needed.

- [Identity Architecture](./identity/index.md)
- [Network Architecture](./network/index.md)
- [Service Architecture](./service/index.md)
- [State Architecture](./state/index.md)

## Intent machine

The Anoma network can be understood as implementing a distributed intent machine. See [10.5281/zenodo.10498992](https://zenodo.org/doi/10.5281/zenodo.10498992) for more details.
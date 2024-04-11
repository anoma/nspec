---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Architecture v1

We first describe on the highest level of abstraction what it means to be a
correct implementation of Anoma and how it is architectured. This already
involves some design choices and assumptions, e.g., about which entities
participate, what actions they can perform, and hardware requirements.

- Host model describes the basic characteristics and functions which
  machines must have in order to run Anoma.
- Primitives describes the basic cryptographic primitives and associated
  assumptions.
- [[Abstractions]] describes the basic abstractions defined by the protocol.
- [[Properties]] describes the properties that the protocol
  should satisfy.

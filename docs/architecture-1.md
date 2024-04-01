# Architecture v1

We first describe on the highest level of abstraction what it means to be a
correct implementation of Anoma and how it is architectured. This already
involves some design choices and assumptions, e.g., about which entities
participate, what actions they can perform, and hardware requirements.

- Host model describes the basic characteristics and functions which
  machines must have in order to run Anoma.
- Primitives describes the basic cryptographic primitives and associated
  assumptions.
- [Abstractions](./architecture-1/abstractions.md) describes the basic abstractions defined by the protocol.
- [Properties](./architecture-1/properties.md) describes the properties that the protocol
  should satisfy.

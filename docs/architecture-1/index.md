---
icon: material/pillar
search:
  exclude: false
  boost: 2
---

# Introduction

We first describe on the highest level of abstraction what it means to be a
correct implementation of Anoma and how it is architectured. This already
involves some design choices and assumptions, e.g., about which entities
participate, what actions they can perform, and hardware requirements.

- [Identity Architecture](./identity/index.md)
- [Network Architecture](./network/index.md)
- [Service Architecture](./service/index.md)
- [State Architecture](./state/index.md)

## Intent machine

The Anoma network can be understood as implementing a distributed intent machine. See [10.5281/zenodo.10498992](https://zenodo.org/doi/10.5281/zenodo.10498992) for more details.
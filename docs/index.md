---
icon: material/home
description: A work-in-progress specification for the Anoma protocol.
social:
  cards: false
search:
    exclude: true
list_wikilinks: false
---

# Anoma Specification

!!! info inline end "Anoma entities"

    The term "Anoma" as used on this site refers specifically to the Anoma Protocol. However, it may
    also be used elsewhere to refer to related entities such as the Anoma
    Network or the Anoma Foundation.

    - The Anoma Network, which consists of nodes using the Anoma protocol.

    - The Anoma Foundation, a Swiss foundation (Stiftung) established to support and coordinate the
    Anoma protocol, network, and the surrounding ecosystem.

    For more information about the foundation, please visit https://anoma.net/learn.

Anoma is a distributed operating system for intent-centric
applications[@goes2024anoma]. The Anoma protocol architecture supports
interoperability at  state, network, and application levels without restricting
the types of intents or computational methods used to solve them.

As a multi-party intent-centric architecture, Anoma is designed for applications
concerned with

- coordination of socio-economic processes dealing with resources,
- distributed capabilities (freedom of action, and control over resources), and
- agreement between agents (users) under conditions of heterogeneous trust.

The same architecture supports both arbitrary fungible measures of value (e.g.
currencies) and unique (non-fungible) objects, so users can choose the
representations and level of precision most appropriate to model aspects of the
world which they care about.

This site aims to describe the architecture required to implement the
Anoma protocol and serves as a guide for Anoma researchers and implementors.

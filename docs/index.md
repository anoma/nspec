---
icon: material/home
description: A work-in-progress specification for the Anoma protocol.
social:
  cards: false
hide:
  - toc
  - tags
tags:
  - index
search:
    exclude: true
---

# Anoma Protocol Specification

!!! info inline end "Anoma entities"

    The term "**Anoma**" as used on this site refers specifically to the **Anoma Protocol**. However, it may
    also be used elsewhere to refer to related entities such as the **Anoma
    Network** or the **Anoma Foundation**.

    - The **Anoma Network**, a network of nodes using the Anoma protocol.

    - The **Anoma Foundation**, a Swiss foundation (Stiftung) established to support and coordinate the
    Anoma protocol, network, and the surrounding ecosystem.

**Anoma** is a distributed operating system for *intent-centric*
applications[@goes2024anoma]. The **Anoma protocol architecture**, object of
this specification, supports interoperability at state, network, and application
levels without restricting the types of intents or computational methods used to
solve them.

As a multi-party intent-centric architecture, Anoma is designed for applications
concerned with:

- Coordination of socio-economic processes dealing with resources,
- distributed capabilities (freedom of action, and control over resources), and
- agreement between agents (users) under conditions of heterogeneous trust.

The same architecture supports both arbitrary *fungible* measures of value (e.g.
currencies) and unique (*non-fungible*) objects, so users can choose the
representations and level of precision most appropriate to model aspects of the
world which they care about.

## Deep diving directions for v0.2

The main controller in v0.2 is a single node, which accepts transaction requests for ordering.
The controller takes care of the resource machine state.
State is organized in terms of persistent resources,
and the state root is what the controller primarily takes care of.
Futher functionality concerns the ordering of incoming transaction requests.

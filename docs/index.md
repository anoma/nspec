---
icon: material/home
description: A work-in-progress specification for the Anoma protocol.
hide:
  - toc
  - navigation
social:
  cards: false
search:
    exclude: true
tags:
    - Anoma
    - Protocol
    - Architecture
    - Applications
    - Intent
---

{@@ if preview @@}
!!! info

{@@ if pull_request @@}
    This is a preview of the Anoma specification using [{@ pr_number @}](https://github.com/anoma/nspec/{@ pr_number @}).
{@@ else @@}
    This is a preview of the Anoma specification using the last commit on the `main` branch.
{@@ endif @@}

{@@ endif @@}

<!-- Source of inspiration:
- https://ethresear.ch/t/rfc-draft-anoma-as-the-universal-intent-machine-for-ethereum/19109
 -->

# Anoma Specification

Anoma is a protocol that serves as a universal standard for developing
blockchain applications. It uses "intents" as building blocks and deploys them
through distributed "intent machines." Anoma supports interoperability at the
state, network, and application levels without restricting the types of intents
or computational methods used to solve them. In order to support the modern
needs of writing these applications, Anoma provides an environment and state
model that manage the complexities of intent-centric, privacy-preserving, and
distributed operations. It also includes a compiler toolchain for writing
intent-based programs in a natural, declarative language, abstracting the
details of compilation to the necessary cryptographic primitives for
privacy-preserving operations.

This site aims to describe the architecture required to implement
the Anoma protocol and serves as a guide for Anoma researchers and implementors.


??? info "Anoma Entities"

    The term "Anoma" as used on this site refers specifically to the Anoma Protocol. However, it may
    also be used elsewhere to refer to related entities such as the Anoma Network or the Anoma
    Foundation.

    - The Anoma Network, which consists of nodes using the Anoma protocol.

    - The Anoma Foundation, a Swiss foundation (Stiftung) established to support and coordinate the
    Anoma protocol, network, and the surrounding ecosystem.

    For more information about the foundation, please visit https://anoma.foundation.

??? question "What is a Protocol?"

    What precisely we mean by "protocol"? As the words are colloquially used, Anoma is closer to a "protocol architecture" or "protocol topology", in that it defines a class of protocols which are unique up to structural isomorphism. If a "protocol" in the TCP/IP sense can be said to consist of a structure and an encoding, where the structure is constrained by the acceptable assumptions and desired properties, but the encoding makes arbitrary decisions about symbolic representation, a "protocol" in the Anoma sense fixes the structure but not the encoding. Any program preserving this structure can be said to implement the Anoma protocol. Standardisation of an encoding is likely in practice, but strictly speaking not even required for distributed consensus - agents must only agree on the encoding and decoding functions on a per-message basis in order to "understand" each other. This disctinction may seem arcane, but it is potentially of practical importance, for a few reasons:


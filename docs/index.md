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

!!! info inline end "Anoma Entities"

    The term "Anoma" as used on this site refers specifically to the Anoma Protocol. However, it may
    also be used elsewhere to refer to related entities such as the Anoma Network or the Anoma
    Foundation.

    - The Anoma Network, which consists of nodes using the Anoma protocol.

    - The Anoma Foundation, a Swiss foundation (Stiftung) established to support and coordinate the
    Anoma protocol, network, and the surrounding ecosystem.

    For more information about the foundation, please visit https://anoma.foundation.

Anoma is a distributed operating system for intent-centric applications[@goes2024anoma]. The protocol architecture supports interoperability at the state,
network, and application levels without restricting the types of intents or computational methods
used to solve them. This site aims to describe the architecture required to implement the Anoma
protocol and serves as a guide for Anoma researchers and implementors.

!!! todo

    J: I want here a clickable diagram that shows the architecture of the Anoma protocol. Which diagram
    should I use? As far as I remember, the following is the most recent one. Is it correct?
    https://research.anoma.net/t/graphing-anoma-agents-v3/341/3

<figure markdown="span">
![Message Diagram](rought_execution_engine_message_passing.svg){ width="450" }
<figcaption markdown="span">
The diagram illustrates the primary components of the Anoma protocol, detailing the architecture of an Anoma node and the interactions between each component within this architecture.
</figcaption>
</figure>

As part of this project, we are also creating additional tools and libraries, including a compiler
toolchain for writing native Anoma intent-based programs in a high-level functional programming
language called [Juvix](https://docs.juvix.org). This compiler toolchain will handle the details of
compiling the necessary cryptographic primitives for privacy-preserving operations. While some
parts of the Anoma protocol are still under development, and some parts contain Juvix code snippets
that describe the intended behaviour of the protocol.


## Table of Contents

{@ dict_to_md(nav_to_dict(navigation)) @}



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

Anoma is a distributed operating system for intent-centric
applications[@goes2024anoma]. The Anoma protocol architecture supports

- interoperability at the state,
- network, and 
- application levels 

without restricting the types of intents or computational methods used to solve
them. 

As a multi-party intent-centric architecture, Anoma is designed for applications
concerned with 

- coordination of socio-economic processes dealing with resources,
- distributed capabilities (freedom of action, and control over resources), and
- agreement between agents (users) under conditions of heterogeneous trust. 

The same architecture supports both arbitrary fungible measures of value (e.g.
currencies) and unique (non-fungible) objects, so users can choose the
representations and level of precision most appropriate to model aspects of the
world which they care about.

<!-- The following is commented for now. The paragraph seems to say many things.
Shorter the better IMO. -->
<!--
Anoma provides a substrate for _information flow control_, giving users
fine-grained control over and the ability to reason about where, when, and to
whom information may be disclosed, subject to whatever trust assumptions they
are willing to make. In order to provide this substrate, Anoma uses many
cryptographic constructions, including public key encryption, one-way hash
functions, succinct non-interactive zero-knowledge proofs, distributed key
generation, threshold encryption, and homomorphic encryption. Anoma's
construction abstracts the underlying primitives by their information-theoretic
properties, so that new primitives may be swapped in overtime.
-->

This site aims to describe the architecture required to implement the
Anoma protocol and serves as a guide for Anoma researchers and implementors.

<!-- The following todo would desapear on the online version. -->

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


## Table of Contents

{@ dict_to_md(nav_to_dict(navigation)) @}



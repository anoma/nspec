---
icon: material/home
description: A work-in-progress specification for the Anoma protocol.
hide:
  - toc
social:
  cards: false
search:
    exclude: true
---

{@@ if version @@}
[{@ version @}](#){ .md-button }
{@@ endif @@}

# Anoma Specification

Anoma is a privacy-preserving, distributed, trust-aware operating system. Like a
typical operating system, Anoma is a platform on top of which applications can
run. It provides memory isolation, inter-application communication, and
execution. Unlike a typical operating system, Anoma is built for multi-party
_intent-centric_ applications. An _intent_, so named because it conveys an
intention, is a message sent by a user describing a preferred state of the
system. After a user sends an intent, two phases take place: _counterparty
discovery_ and _settlement_. In the _counterparty discovery_ phase, network
participants examine and match compatible intents, forming transactions which
enact particular state changes. Transactions then enter the _settlement_ phase
for ordering, execution, and confirmation by consensus, after which users can
read the updated state. Anoma assumes a model of _heterogeneous trust_, where
users express trust preferences in their intents, only intents with compatible
trust preferences can be matched, and consensus rounds are performed on demand
to facilitate settlement. To applications, Anoma provides a host environment and
state model that handle all of the complex parts of intent-centric,
privacy-preserving, and distributed operation. Anoma also comes with a compiler
toolchain which allows developers to write Anoma-compatible programs in
high-level languages, abstracting the particulars of compilation to the
cryptographic primitives required for privacy-preserving operation. This
standardisation allows developers to focus on their application-specific logic
and enables applications to interoperate in both the counterparty discovery and
settlement phases.

Anoma's multi-party intent-centric architecture is designed for applications
concerned with coordination of socio-economic processes dealing with resources,
distributed capabilities (freedom of action, and control over resources), and
agreement between agents (users) under conditions of heterogeneous trust.
_Intents_ are computable predicates over possible states of the ledger which
convey underlying human intentions or preferences. Anoma supports both arbitrary
fungible measures of value (e.g. currencies) and unique (non-fungible) objects,
so users can choose the representations and level of precision most appropriate
to model aspects of the world which they care about.

Anoma provides a substrate for _information flow control_, giving users
fine-grained control over and the ability to reason about where, when, and to
whom information may be disclosed, subject to whatever trust assumptions they
are willing to make. In order to provide this substrate, Anoma uses many
cryptographic constructions, including public key encryption, one-way hash
functions, succinct non-interactive zero-knowledge proofs, distributed key
generation, threshold encryption, and homomorphic encryption. Anoma's
construction abstracts the underlying primitives by their information-theoretic
properties, so that new primitives may be swapped in over time.

<!--

Anoma draws upon and synthesises prior art in the broad areas of distributed ledger architecture, cybernetic systems design, monetary anthropology, and web-of-trust construction. It relies upon results, primitives, and constructions from the academic research fields of distributed systems, cryptography, computational complexity theory, information theory, algorithmic game theory, programming language theory, and category theory, among others. Readers with expertise in one or more of these areas or fields may find it helpful to understand Anoma in relation to them.Descriptions of some of these relational structures can be found in the [angles of approach](./angles-of-approach.md#angles-of-approach) section.

-->

These documents describe Anoma. They are intended to be _complete_, in that
enough is said to define precisely what a valid implementation of Anoma must do,
and _minimal_, in that no more is said than that.

Anoma is free, in both the senses of "free speech" and "free beer". The source
for these documents is [on Github](https://github.com/anoma/specs), permissively
licensed, and they can be forked or edited as you like. At present, this
particular repository is stewarded by the [Anoma
Foundation](https://anoma.foundation/). Contributions are welcome.

!!! note

    For clarity, the word "Anoma" is used to refer to three separate but related entities:
    - The Anoma _protocol_, which is defined in this specification.
    - The Anoma _network_, which is the network of nodes using the Anoma protocol.
    - The Anoma _Foundation_, which is a Swiss foundation (Stiftung) chartered with support & coordination of the Anoma protocol, network, and surrounding ecosystem.
     <br /><br/>
    These documents describe the protocol only, not the network or the foundation. To learn more about the foundation, go [here](https://anoma.foundation).
    <br/><br/>In these documents, the word "Anoma" alone refers to the Anoma protocol.

!!! note

    What precisely we mean by "protocol"? As the words are colloquially used, Anoma is closer to a "protocol architecture" or "protocol topology", in that it defines a class of protocols which are unique up to structural isomorphism. If a "protocol" in the TCP/IP sense can be said to consist of a structure and an encoding, where the structure is constrained by the acceptable assumptions and desired properties, but the encoding makes arbitrary decisions about symbolic representation, a "protocol" in the Anoma sense fixes the structure but not the encoding. Any program preserving this structure can be said to implement the Anoma protocol. Standardisation of an encoding is likely in practice, but strictly speaking not even required for distributed consensus - agents must only agree on the encoding and decoding functions on a per-message basis in order to "understand" each other. This disctinction may seem arcane, but it is potentially of practical importance, for a few reasons:

    - A third party observing the cleartext part of the communications between two agents may not easily be able to detect whether or not they are even speaking the Anoma protocol if they do not know the specific encoding in use.

    - The Anoma protocol may be "disguised" as any sufficently general existing protocol (e.g. HTTP) in a way which cannot be automatically detected.

!!! note

    These documents are not yet complete. If you're reading this page right now, there's a high chance you might be interested in [Namada](https://namada.net).

Happy reading!

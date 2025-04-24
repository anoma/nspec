---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - concept
  - engine
---

# The concept of an engine

## Overview

The model of Anoma revolves around the concept of an [[Engine|engine]] instance, an
actor-like entity encapsulating all aspects of a computation process.

An engine has the following components:

- a declaration of a **message interface**,
- a [[Engine Configuration|configuration]],
- an [[Engine Environment|environment]], and
- a [[Engine Behaviour|behaviour]].

Engines of the same type share the same [[Engine Behaviour|behaviour]]. However, two engines of the same type may have different
[[Engine Environment|execution context]],
which in turn may lead to a different message reaction pattern
(as "observed" by other engines).

We often write _engine_,
whenever the context makes clear that we refer to a _term_ of an engine type
(and not to the type itself),
for the sake of brevity.

## The type of an engine

The type of engines is defined in the [[Engine|engine]] module.
We show the type definition here for convenience.

--8<-- "./docs/arch/node/types/engine.juvix.md:Engine"

## Engine components

### [[Engine Configuration|*Configuration*]]

The configuration of an engine. The data of an engine configuration consists of:

- a parent engine,
- a name,
- a node ID, and
- a generic configuration type `c`.

The complete definition of an engine configuration can be found in the
[[Engine Configuration|Juvix engine configuration definition]].

### [[Engine Environment|*Environment*]]

The execution context of an engine. The data of an engine environment consists of:

- a local state for storing engine-specific data,
- a mailbox cluster for receiving and sending [[Anoma Message|messages]],
- a set of acquaintances (other engines that can interact with this engine), and
- a set of active timers.

The complete definition of an engine environment can be found in the
[[Engine Environment|Juvix engine environment definition]].

### [[Engine Behaviour|*Behaviour*]]

The function that describes all possible ways in which engines react to
messages. This includes:

- modifying their environment,
- sending messages to other engines,
- spawning new engine instances, and
- managing their active timers.

The complete definition of an engine behaviour can be found in the
[[Engine Behaviour|Juvix engine behaviour definition]].

## Useful Links

- Learn about the [[Anomian]].
- [[Engines in Anoma|Tutorials on Writing Engine Families for Anoma Spec writers]].
- [[Ticker Engine|Example of an engine that ticks, the Ticker Engine]].

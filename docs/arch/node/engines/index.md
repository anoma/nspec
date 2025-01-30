---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - concept
  - engine
  - type
---

# Engines

## Overview

The Anoma Specification revolves around the concept of an [[Engine|engine]], an
actor-like entity encapsulating the [[Engine Environment|engine environment]] and
[[Engine Behaviour|behaviour]] of a computational process. In Anoma, every
engine is of a specific type. Engines of the same type share the same
[[Engine Behaviour|behaviour]]. However, two engines of the same type may have different
[[Engine Environment|execution context]].


## Engine components

[[Engine Environment|*Environment*]]

:   The execution context of an engine. It consists of:

    - a local state for storing engine-specific data,
    - a mailbox cluster for receiving and sending [[Anoma Message|messages]],
    - a set of acquaintances (other engines that can interact with this engine), and
    - a set of active timers.

    The complete definition of an engine environment can be found in the
    [[Engine Environment|Juvix engine environment definition]].

[[Engine Behaviour|*Behaviour*]]

:   The function that describes all possible ways in which engines can act. This
includes:

    - modifying their environment,
    - sending messages to other engines,
    - spawning new engine instances, and
    - managing their active timers.

    The complete definition of an engine behaviour can be found in the
    [[Engine Behaviour|Juvix engine behaviour definition]].

    [[Engine Behaviour#Guard|*Guards*]]

    :   The finite set of guard functions that describe the conditions under which
        the local state of the engine's instance should change by invoking the action
        function.

    [[Engine Behaviour#conflict-resolution|*Conflict Solver*]]

    :   The function that resolves conflicts between actions to maximize their
        concurrency.


## Anoma engine definitions

All required types and functions to define these engines can be found in the
module [[Engine Types|engine]]. To understand how we have structured the
definitions of engine types, see [[Engines in Anoma|Tutorials on Writing
Engine Families]] and [[Anomian]].

### [[Anoma Message|Anoma engine messages]]

--8<-- "./anoma_message.juvix.md:Msg"

### [[Anoma Configuration|Anoma engine configurations]]

--8<-- "./anoma_config.juvix.md:Cfg"

### [[Anoma Environment|Anoma engine environments]]

--8<-- "./anoma_environment.juvix.md:Env"

## Useful Links

- [[Anomian]]
- [[Engines in Anoma|Tutorials on Writing Engine Families]]
- [[Ticker Engine|Example Engine]]
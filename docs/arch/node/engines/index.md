---
icon: octicons/gear-16
search:
exclude: false
tags:
  - engine
  - Juvix
---

# Engines

## Overview

The Anoma Specification revolves around the concept of an [[Engine|engine]], an
actor-like entity encapsulating the [[Engine Environment|engine environment]] and
[[Engine Behaviour|behaviour]] of a computational process. In Anoma, engines are
organised into families based on shared [[Engine Behaviour|behaviour]].
Although, each of these engines has its own [[Engine Environment|execution context]].

The components of an engine are:

[[Engine Environment]]

:   The execution context of an engine. It consists of:
    - a local state for storing engine-specific data,
    - a mailbox cluster for receiving and sending messages,
    - a set of acquaintances (other engines that can interact with this engine), and
    - a set of active timers.

    The complete definition of an engine environment can be found in the
    [[Engine Environment|Juvix engine environment definition]].

[[Engine Behaviour|*Action Function*]]

:   The function that describes all possible ways in which engines can act. This includes:
    - modifying their environment,
    - sending messages to other engines,
    - spawning new engine instances, and
    - managing their active timers.

    The complete definition of an engine dynamics can be found in the
    [[Engine Behaviour|Juvix engine dynamics definition]].

    *Guards*

    :   The finite set of guard functions that describe the conditions under which
        the local state of the engine's instance should change by invoking the action
        function.

    *Conflict Solver*

    :   The function that resolves conflicts between actions to maximize their
        concurrency.

## Juvix engine definitions

For the Anoma Specification, engines are written in Juvix Markdown. All
necessary types and functions to define these engines can be found in the module
[[Engine Types|engine]]. See [[Engines in Anoma|Tutorials on Writing Engine
Families]] for a tutorial on how to structure the writing of engine families for
the Anoma Specification.

### Anoma engine messages

    --8<-- "./docs/arch/node/types/anoma_message.juvix.md"

### Anoma engine environments

    --8<-- "./docs/arch/node/types/anoma_environment.juvix.md"

## Useful Links

- [[Engines in Anoma|Tutorials on Writing Engine Families]]
- [[Ticker Engine|Example Engine]]
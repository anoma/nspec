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

The Anoma Specification revolves around the concept of an _engine_, an
actor-like entity encapsulating the state and behaviour of a computational
process. Engines operate within a specific execution context called the _engine
environment_. In Anoma, engines are organised into families based on shared
behaviour and environment, although each engine instance has its own local state and
name.

Each engine must declare specific _components_ that each of its member
engine instances will have. For Anoma specifications, the components are:

[[Engine Environment]]

:   This serves as the execution context for engines. In addition to the local
    state, the engine environment encompasses elements such as the mailbox
    cluster owned by an engine instance and a finite set of acquaintances—other
    engine instances known to the current one that can interact with it.

    - [[Engine Environment|Juvix engine environment definition]]

[[Engine Behaviour|*Action Function*]]

:   The function that describes all possible ways in which engines can act, by
    changing their environment, sending messages, spawning new engine instances,
    and update their list of active timers.

    - [[Engine Dynamics|Juvix engine dynamics definition]]

    *Guards*

    :   The finite set of guard functions that describe the conditions under which
        the local state of the engine's instance should change by invoking the action
        function.

    *Conflict Solver*

    :   The function that resolves conflicts between actions to maximize their
        concurrency.

## Juvix engine definitions

For the Anoma Specification, engines are written in Juvix Markdown.
All necessary types and functions to define these engines can be found
in the module [[Engine Types|engine]].
See [[Engines in Anoma|Tutorials on Writing Engine Families]]
for a tutorial on how to structure the writing of engine families in Juvix.

Below we showcase the _current_ engine families and their related components in
Juvix for the Anoma Specification. Please be aware that not all engine families
are listed here, and the specification is continually expanding with new engine
families.

??? quote "Engine messages in Anoma"

    --8<-- "./docs/arch/node/types/anoma_message.juvix.md"

??? quote "Engine environments in Anoma"

    --8<-- "./docs/arch/node/types/anoma_environment.juvix.md"

## Useful Links

- [[Engines in Anoma|Tutorials on Writing Engine Families]]
- [[Ticker Engine|Example Engine]]
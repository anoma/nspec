---
icon: octicons/gear-16
search:
exclude: false
tags:
  - engine-family
  - Juvix
---

# Engine Families

## Overview

The Anoma Specification revolves around the concept of an _engine_, an
actor-like entity encapsulating the state and behaviour of a computational
process. Engines operate within a specific execution context called the _engine
environment_. In Anoma, engines are organised into families based on shared
behaviour and environment, although each instance has its own local state and
name.

Each engine family must declare specific _components_ that each of its member
engine instances will have. For Anoma specifications, the components are:

*Engine Environment*

:   This serves as the execution context for engines. In addition to the local
    state, the engine environment encompasses elements such as the mailbox
    cluster owned by an engine instance and a finite set of acquaintances—other
    engine instances known to the current one that can interact with it.

*Action Function*

:   The function that describes all possible ways in which engines can act, by
    changing their environment, sending messages, spawning new engine instances,
    and update their list of active timers.

*Guards*

:   The finite set of guard functions that describe the conditions under which
    the local state of the engine's instance should change by invoking the action
    function.

*Conflict Solver*

:   The function that resolves conflicts between actions to maximize their
    concurrency.

## Juvix Engine Families

For the Anoma Specification, engine families are written in Juvix. All necessary
types and functions to define these engines can be found in the module
[[Engine Family Types|node_architecture.types.engine_family]].(1)
{.annotate }

  1.  For a tutorial on how to structure the writing of engine families in
      Juvix, see [[ Engines in Anoma ]].

Below we showcase the _current_ engine families and their related components in
Juvix for the Anoma Specification. Please be aware that not all engine families
are listed here, and the specification is continually expanding with new engine
families.


??? info "AnomaEngine"

    --8<-- "./docs/node_architecture/types/anoma_engine.juvix.md"

??? info "AnomaMessage"

    --8<-- "./docs/node_architecture/types/anoma_message.juvix.md"

??? info "AnomaEnvironment"

    --8<-- "./docs/node_architecture/types/anoma_environment.juvix.md"


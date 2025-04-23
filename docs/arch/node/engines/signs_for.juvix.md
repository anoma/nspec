---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - signsfor
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.signs_for_config open public;
    import arch.node.engines.signs_for_messages open public;
    import arch.node.engines.signs_for_environment open public;
    import arch.node.engines.signs_for_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open signs_for_config_example;
    open signs_for_environment_example;
    ```

# SignsFor Engine

The SignsFor Engine manages signs for relationships between identities.
A "signs for" relationship indicates that one identity can produce signatures
(commitments) on behalf of another identity.

## Purpose

The SignsFor Engine maintains and manages the state of sings for relationships between
identities. It handles queries about these relationships, allows submission of new
evidence, and provides information about existing relationships. This is useful in
scenarios where signature delegation or proxy signing is required.

## Engine components

- [[SignsFor Messages]]
- [[SignsFor Configuration]]
- [[SignsFor Environment]]
- [[SignsFor Behaviour]]

## Type

<!-- --8<-- [start:SignsForEngine] -->
```juvix
SignsForEngine : Type :=
  Engine
    SignsForCfg
    SignsForLocalState
    SignsForMailboxState
    SignsForTimerHandle
    SignsForActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:SignsForEngine] -->

### Example of a signsFor engine

<!-- --8<-- [start:exampleSignsForEngine] -->
```juvix
exampleSignsForEngine : SignsForEngine :=
  Engine.mk@{
    cfg := signsForCfg;
    env := signsForEnv;
    behaviour := signsForBehaviour;
  };
```
<!-- --8<-- [end:exampleSignsForEngine] -->

where `signsForCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/signs_for_config.juvix.md:signsForCfg"

`signsForEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/signs_for_environment.juvix.md:signsForEnv"

and `signsForBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/signs_for_behaviour.juvix.md:signsForBehaviour"

---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- signs-for-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.signs_for_messages open public;
    import arch.node.engines.signs_for_environment open public;
    import arch.node.engines.signs_for_behaviour open public;
    open signs_for_environment_example;
    ```

# SignsFor Engine

The Signs For Engine manages signs for relationships between identities.
A "signs for" relationship indicates that one identity can produce signatures
(commitments) on behalf of another identity.

## Purpose

The Signs For Engine maintains and manages the state of sings for relationships between
identities. It handles queries about these relationships, allows submission of new
evidence, and provides information about existing relationships. This is useful in
scenarios where signature delegation or proxy signing is required.

## Components

- [[SignsFor Messages]]
- [[SignsFor Environment]]
- [[SignsFor Behaviour]]

## Type

<!-- --8<-- [start:SignsForEngine] -->
```juvix
SignsForEngine : Type :=
  Engine
    SignsForLocalState
    SignsForMailboxState
    SignsForTimerHandle
    SignsForMatchableArgument
    SignsForActionLabel
    SignsForPrecomputation;
```
<!-- --8<-- [end:SignsForEngine] -->

### Example of a signsFor engine

```juvix extract-module-statements
exampleSignsForEngine : SignsForEngine := mkEngine@{
    name := "signsFor";
    initEnv := signsForEnvironment;
    behaviour := signsForBehaviour;
  };
```

where `signsForEnvironment` is defined as follows:

--8<-- "./docs/arch/node/engines/signs_for_environment.juvix.md:signsForEnvironment"

and `commitmentBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/signs_for_environment.juvix.md:signsForBehaviour"

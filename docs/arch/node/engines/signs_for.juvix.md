---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- signsFor
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.signsFor;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.signs_for_messages open public;
    import arch.node.engines.signs_for_environment open public;
    import arch.node.engines.signs_for_behaviour open public;
    open signs_for_environment_example;
    ```

# SignsFor Engine

???

## Purpose

???

## Components

- [[SignsFor Messages]]
- [[SignsFor Environment]]
- [[SignsFor Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:SignsForEngine] -->
```juvix
SignsForEngine : Type := Engine
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
    behaviour := signsForBehaviour;
    initEnv := signsForEnvironmentExample;
  };
```

where `signsForEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/signsFor_environment.juvix.md:environment-example"

---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- reads_for
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.reads_for_messages open public;
    import arch.node.engines.reads_for_environment open public;
    import arch.node.engines.reads_for_behaviour open public;
    open reads_for_environment_example;
    ```

# ReadsFor Engine

The Reads For Engine manages `reads_for` relationships between identities. A `reads_for` relationship indicates that one identity can read data encrypted for another identity.

## Purpose

The Reads For Engine maintains and manages the state of `reads_for` relationships between identities. It handles queries about these relationships, allows submission of new evidence, and provides information about existing relationships. This is useful in scenarios where data access needs to be delegated or shared.

## Components

- [[ReadsFor Messages]]
- [[ReadsFor Environment]]
- [[ReadsFor Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:ReadsForEngine] -->
```juvix
ReadsForEngine : Type := Engine
  ReadsForLocalState
  ReadsForMailboxState
  ReadsForTimerHandle
  ReadsForMatchableArgument
  ReadsForActionLabel
  ReadsForPrecomputation;
```
<!-- --8<-- [end:ReadsForEngine] -->

### Example of a readsFor engine

```juvix extract-module-statements
exampleReadsForEngine : ReadsForEngine :=
  mkEngine@{
    behaviour := readsForBehaviour;
    initEnv := readsForEnvironmentExample;
  };
```

where `readsForEnvironmentExample` is defined as follows:

--8<-- "./reads_for_environment.juvix.md:environment-example"

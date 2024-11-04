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

## Purpose

The Reads For Engine tracks `reads_for` relationships between identities. It supports querying which identities read for another identity or can read for it, submitting evidence that one identity reads for another, and querying evidence concerning known `reads_for` relationships.

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
exampleReadsForEngine : ReadsForEngine := mkEngine@{
    name := "readsFor";
    behaviour := readsForBehaviour;
    initEnv := readsForEnvironmentExample;
  };
```

where `readsForEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/readsFor_environment.juvix.md:environment-example"

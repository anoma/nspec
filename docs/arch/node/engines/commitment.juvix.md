---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- commitment
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.commitment;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.commitment_messages open public;
    import arch.node.engines.commitment_environment open public;
    import arch.node.engines.commitment_behaviour open public;
    open commitment_environment_example;
    ```

# Commitment Engine

???

## Purpose

???

## Components

- [[Commitment Messages]]
- [[Commitment Environment]]
- [[Commitment Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:CommitmentEngine] -->
```juvix
CommitmentEngine : Type := Engine
  CommitmentLocalState
  CommitmentMailboxState
  CommitmentTimerHandle
  CommitmentMatchableArgument
  CommitmentActionLabel
  CommitmentPrecomputation;
```
<!-- --8<-- [end:CommitmentEngine] -->

### Example of a commitment engine

```juvix extract-module-statements
exampleCommitmentEngine : CommitmentEngine := mkEngine@{
    name := "commitment";
    behaviour := commitmentBehaviour;
    initEnv := commitmentEnvironmentExample;
  };
```

where `commitmentEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/commitment_environment.juvix.md:environment-example"

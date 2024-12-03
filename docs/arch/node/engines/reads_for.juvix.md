---
icon: octicons/project-template-24
search:
  exclude: false
categories:
- engine
tags:
- reads-for-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.reads_for_messages open public;
    import arch.node.engines.reads_for_environment open public;
    import arch.node.engines.reads_for_behaviour open public;

    import arch.node.engines.reads_for_config open public;
    import arch.node.engines.reads_for_messages open public;
    import arch.node.engines.reads_for_environment open public;
    import arch.node.engines.reads_for_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open reads_for_config_example;
    open reads_for_environment_example;
    ```

# Reads For Engine

The Reads For Engine manages `reads_for` relationships between identities. A
`reads_for` relationship indicates that one identity can read data encrypted
for another identity.

## Purpose

The Reads For Engine maintains and manages the state of `reads_for`
relationships between identities. It handles queries about these relationships,
allows submission of new evidence, and provides information about existing
relationships. This is useful in scenarios where data access needs to be
delegated or shared.

## Components

- [[Reads For Messages]]
- [[Reads For Config]]
- [[Reads For Environment]]
- [[Reads For Behaviour]]

## Type

<!-- --8<-- [start:ReadsForEngine] -->
```juvix
ReadsForEngine : Type :=
  Engine
    ReadsForCfg
    ReadsForLocalState
    ReadsForMailboxState
    ReadsForTimerHandle
    ReadsForActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:ReadsForEngine] -->

### Example of a reads for engine

<!-- --8<-- [start:exampleReadsForEngine] -->
```juvix
exampleReadsForEngine : ReadsForEngine :=
  mkEngine@{
    cfg := readsForCfg;
    env := readsForEnv;
    behaviour := readsForBehaviour;
  };
```
<!-- --8<-- [end:exampleReadsForEngine] -->

where `readsForCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/reads_for_config.juvix.md:readsForCfg"

`readsForEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/reads_for_environment.juvix.md:readsForEnv"

and `readsForBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/reads_for_behaviour.juvix.md:readsForBehaviour"

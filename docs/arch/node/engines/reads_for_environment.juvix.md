---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- reads_for
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for_environment;

    import prelude open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.reads_for_messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# ReadFor Environment

## Overview

The ReadFor Engine environment maintains the state necessary for managing `reads_for` relationships between identities, including storing evidence submitted by clients.

??? quote "Auxiliary Juvix code"

    ```juvix
    axiom verifyEvidence : ReadsForEvidence -> Bool;
    ```

## Mailbox states

The ReadFor Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `ReadsForMailboxState`

```juvix
syntax alias ReadsForMailboxState := Unit;
```

## Local state

The local state of the ReadFor Engine includes the evidence for reads_for relationships.

### `ReadsForLocalState`

```juvix
type ReadsForLocalState := mkReadsForLocalState@{
  evidenceStore : Set ReadsForEvidence;
};
```

???+ quote "Arguments"

    `evidenceStore`:
    : The collection of validated `ReadsForEvidence` which has been submitted to the engine.

## Timer Handle

The ReadFor Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

### `ReadsForTimerHandle`

```juvix
syntax alias ReadsForTimerHandle := Unit;
```

## The ReadFor Environment

### `ReadsForEnv`

```juvix
ReadsForEnv : Type :=
  EngineEnv
    ReadsForLocalState
    ReadsForMailboxState
    ReadsForTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:readsForEnv] -->
```juvix extract-module-statements
module reads_for_environment_example;

readsForEnv : ReadsForEnv :=
    mkEngineEnv@{
      localState := mkReadsForLocalState@{
        evidenceStore := Set.empty;
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:readsForEnv] -->
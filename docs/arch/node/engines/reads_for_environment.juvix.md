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

# Reads For Environment

## Overview

The Reads For Engine environment maintains the state necessary for managing `reads_for` relationships between identities, including storing evidence submitted by clients.

## Mailbox states

The Reads For Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `ReadsForMailboxState`

```juvix
syntax alias ReadsForMailboxState := Unit;
```

## Local state

The local state of the Reads For Engine includes the evidence for reads_for relationships.

### `ReadsForLocalState`

```juvix
type ReadsForLocalState := mkReadsForLocalState@{
  evidenceStore : Set ReadsForEvidence;
  verifyEvidence : ReadsForEvidence -> Bool;
};
```

???+ quote "Arguments"

    `evidenceStore`:
    : The collection of validated `ReadsForEvidence` which has been submitted to the engine.

    `verifyEvidence`:
    : Function to validate submitted `ReadsForEvidence`.

## Timer Handle

The Reads For Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

### `ReadsForTimerHandle`

```juvix
syntax alias ReadsForTimerHandle := Unit;
```

## The Reads For Environment

### `ReadsForEnvironment`

```juvix
ReadsForEnvironment : Type :=
  EngineEnv
    ReadsForLocalState
    ReadsForMailboxState
    ReadsForTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:readsForEnvironment] -->
```juvix extract-module-statements
module reads_for_environment_example;

readsForEnvironment : ReadsForEnvironment :=
    mkEngineEnv@{
      localState := mkReadsForLocalState@{
        evidenceStore := Set.empty;
        verifyEvidence := \{ _ := true }
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:readsForEnvironment] -->
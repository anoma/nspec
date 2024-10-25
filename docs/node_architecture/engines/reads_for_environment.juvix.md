---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-family
tags:
- reads_for
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.reads_for_environment;

    import prelude open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identities open;
    import node_architecture.identity_types open;
    import node_architecture.engines.reads_for_overview open;
    ```

# Reads For Environment

## Overview

The Reads For Engine environment maintains the state necessary for managing `reads_for` relationships between identities, including storing evidence submitted by clients.

## Mailbox states

The Reads For Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias ReadsForMailboxState := Unit;
```

## Local state

The local state of the Reads For Engine includes the evidence for reads_for relationships.

```juvix
type ReadsForLocalState := mkReadsForLocalState {
  evidenceStore : Set ReadsForEvidence;
  verifyEvidence : ReadsForEvidence -> Bool;
};
```

## Timer Handle

```juvix
syntax alias ReadsForTimerHandle := Unit;
```

The Reads For Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
ReadsForEnvironment : Type := EngineEnvironment
  ReadsForLocalState
  ReadsForMailboxState
  ReadsForTimerHandle;
```

## Example of a `Reads For` environment

```juvix extract-module-statements
module reads_for_environment_example;

readsForEnvironmentExample : ReadsForEnvironment :=
    mkEngineEnvironment@{
      name := "reads_for";
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

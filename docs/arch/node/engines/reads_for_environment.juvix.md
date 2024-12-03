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
type ReadsForLocalState := mkReadsForLocalState@{
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
ReadsForEnvironment : Type := EngineEnv
  ReadsForLocalState
  ReadsForMailboxState
  ReadsForTimerHandle;
```

## Example of a `Reads For` environment

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module reads_for_environment_example;

readsForEnvironmentExample : ReadsForEnvironment :=
    mkEngineEnv@{
      node := Curve25519PubKey "0xabcd1234";
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
<!-- --8<-- [end:environment-example] -->

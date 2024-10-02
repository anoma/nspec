---
icon: octicons/gear-16
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
    import node_architecture.types.identity_types open;
    import node_architecture.engines.reads_for_overview open;
    ```
    
# Reads For Engine Environment

## Overview

The Reads For Engine maintains the state necessary for managing `reads_for` relationships between identities, including storing evidence submitted by clients.

## Mailbox States

The Reads For Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias ReadsForMailboxState := Unit;
```

## Local State

The local state of the Reads For Engine includes the evidence for reads_for relationships.

```juvix
type ReadsForLocalState := mkReadsForLocalState {
  evidenceStore : Set ReadsForEvidence;
};
```

## Timer Handles

The Reads For Engine does not require timers. We define the timer handle type as Unit.

```juvix
syntax alias ReadsForTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
ReadsForEnvironment : Type := EngineEnvironment
  ReadsForLocalState
  ReadsForMsg
  ReadsForMailboxState
  ReadsForTimerHandle;
```

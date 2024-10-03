---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- signs_for
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.signs_for_environment;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.signs_for_overview open;
    ```
    
# Signs For Engine Environment

## Overview

The Signs For Engine maintains the state necessary for managing `signs_for` relationships between identities, including storing evidence submitted by clients.

## Mailbox States

The Signs For Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias SignsForMailboxState := Unit;
```

## Local State

The local state of the Signs For Engine includes the evidence for signs_for relationships.

```juvix
type SignsForLocalState := mkSignsForLocalState {
  evidenceStore : Set SignsForEvidence;
};
```

## Timer Handles

The Signs For Engine does not require timers. We define the timer handle type as `Unit`.

```juvix
syntax alias SignsForTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
SignsForEnvironment : Type := EngineEnvironment
  SignsForLocalState
  SignsForMsg
  SignsForMailboxState
  SignsForTimerHandle;
```

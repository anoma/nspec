---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - signsfor
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for_environment;

    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.signs_for_messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# SignsFor Environment

## Overview

The SignsFor Engine environment maintains the state necessary for managing `signs_for` relationships between identities, including storing evidence submitted by clients.

??? quote "Auxiliary Juvix code"

    ```juvix
    axiom verifyEvidence : SignsForEvidence -> Bool;
    ```

## Mailbox states

The SignsFor Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `SignsForMailboxState`

```juvix
syntax alias SignsForMailboxState := Unit;
```

## Local state

The local state of the SignsFor Engine includes the evidence for signs_for relationships.

### `SignsForLocalState`

```juvix
type SignsForLocalState := mkSignsForLocalState@{
  evidenceStore : Set SignsForEvidence;
};
```

???+ quote "Arguments"

    `evidenceStore`:
    : The collection of validated `SignsForEvidence` which has been submitted to the engine.

## Timer Handle

The SignsFor Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

### `SignsForTimerHandle`

```juvix
syntax alias SignsForTimerHandle := Unit;
```

## The SignsFor Environment

### `SignsForEnv`

```juvix
SignsForEnv : Type :=
  EngineEnv
    SignsForLocalState
    SignsForMailboxState
    SignsForTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:signsForEnv] -->
```juvix extract-module-statements
module signs_for_environment_example;

signsForEnv : SignsForEnv :=
    mkEngineEnv@{
      localState := mkSignsForLocalState@{
        evidenceStore := Set.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:signsForEnv] -->

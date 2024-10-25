---
icon: octicons/container-24
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
    import node_architecture.types.messages open;
    import node_architecture.types.engine_environment open;
    import node_architecture.identity_types open;
    import node_architecture.engines.signs_for_overview open;
    ```

# Signs For Environment

## Overview

The Signs For Engine environment maintains the state necessary for managing `signs_for` relationships between identities, including storing evidence submitted by clients.

## Mailbox states

The Signs For Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias SignsForMailboxState := Unit;
```

## Local state

The local state of the Signs For Engine includes the evidence for signs_for relationships.

```juvix
type SignsForLocalState := mkSignsForLocalState {
  evidenceStore : Set SignsForEvidence;
  verifyEvidence : SignsForEvidence -> Bool;
};
```

## Timer Handle

```juvix
syntax alias SignsForTimerHandle := Unit;
```

The Signs For Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
SignsForEnvironment : Type := EngineEnvironment
  SignsForLocalState
  SignsForMailboxState
  SignsForTimerHandle;
```

## Example of a `Signs For` environment

```juvix extract-module-statements
module signs_for_environment_example;

signsForEnvironmentExample : SignsForEnvironment :=
    mkEngineEnvironment@{
      name := "signs_for";
      localState := mkSignsForLocalState@{
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

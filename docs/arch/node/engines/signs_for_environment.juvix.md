---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- signs_for
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for_environment;

    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.signs_for_messages open;
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
type SignsForLocalState := mkSignsForLocalState@{
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

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module signs_for_environment_example;

signsForEnvironmentExample : SignsForEnvironment :=
    mkEngineEnvironment@{
      node := Curve25519PubKey "0xabcd1234";
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
<!-- --8<-- [end:environment-example] -->

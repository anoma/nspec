---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - verification
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.verification_environment;

    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.verification_messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Verification Environment

## Overview

The Verification Engine is stateless and does not maintain any internal state between requests. It relies on external information (like the `signs_for` relationships) for its operations.

## Mailbox states

The Verification Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `VerificationMailboxState`

```juvix
syntax alias VerificationMailboxState := Unit;
```

## Local state

The local state of a Verification Engine instance contains a map to a list of pending requests which require `SignsFor` information which is requested from the associated `SignsFor` engine.

### `VerificationLocalState`

```juvix
type VerificationLocalState := mkVerificationLocalState@{
  pendingRequests : Map ExternalIdentity (List (Pair EngineID (Pair Signable Commitment)));
};
```

???+ code "Arguments"

    `pendingRequests`:
    : The backlog of verification requests still in processing.

## Timer Handle

The Verification Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

### `VerificationTimerHandle`

```juvix
syntax alias VerificationTimerHandle := Unit;
```

## The Verification Environment

### `VerificationEnv`

```juvix
VerificationEnv : Type :=
  EngineEnv
    VerificationLocalState
    VerificationMailboxState
    VerificationTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:verificationEnv] -->
```juvix extract-module-statements
module verification_environment_example;

verificationEnv : VerificationEnv :=
    mkEngineEnv@{
      localState := mkVerificationLocalState@{
        pendingRequests := Map.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:verificationEnv] -->

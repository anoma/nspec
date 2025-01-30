---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - encryption
  - environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.encryption_environment;

    import prelude open;
    import arch.node.engines.encryption_messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# `Encryption` Engine Environment

## Overview

The `Encryption` Engine is stateless and does not maintain any internal state
between requests. It relies on external information (like the `reads_for`
relationships) for its operations.

## Mailbox states

The `Encryption` Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `EncryptionMailboxState`

```juvix
syntax alias EncryptionMailboxState := Unit;
```

## Local state

The local state of an `Encryption` Engine instance contains a map to a list of pending requests which
require `ReadsFor` information which is requested from the associated `ReadsFor`
engine.

### `EncryptionLocalState`

```juvix
type EncryptionLocalState := mkEncryptionLocalState@{
  pendingRequests : Map ExternalIdentity (List (Pair EngineID Plaintext));
};
```

???+ quote "Arguments"

    `pendingRequests`:
    : The backlog of encryption requests still in processing.

## Timer Handle

The Encryption Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

### `EncryptionTimerHandle`

```juvix
syntax alias EncryptionTimerHandle := Unit;
```

## The Encryption Environment

### `EncryptionEnv`

```juvix
EncryptionEnv : Type :=
  EngineEnv
    EncryptionLocalState
    EncryptionMailboxState
    EncryptionTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:encryptionEnv] -->
```juvix extract-module-statements
module encryption_environment_example;

encryptionEnv : EncryptionEnv :=
    mkEngineEnv@{
      localState := mkEncryptionLocalState@{
        pendingRequests := Map.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:encryptionEnv] -->
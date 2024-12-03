---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- decryption
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.decryption_environment;
    import prelude open;
    import arch.node.engines.decryption_messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Decryption Environment

## Overview

Each Decryption Engine instance is associated with a specific identity and
handles decryption requests for that identity. The environment maintains the
necessary state for decryption operations.

## Mailbox states

The Decryption Engine does not require complex mailbox states. We define the
mailbox state as `Unit`.

### `DecryptionMailboxState`

```juvix
syntax alias DecryptionMailboxState := Unit;
```

## Local state

The decryption engine is stateless.

### `DecryptionLocalState`

```juvix
syntax alias DecryptionLocalState := Unit;
```

## Timer Handle

The Decryption Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

### `DecryptionTimerHandle`

```juvix
syntax alias DecryptionTimerHandle := Unit;
```

## The Decryption Environment

### `DecryptionEnv`

```juvix
DecryptionEnv : Type :=
  EngineEnv
    DecryptionLocalState
    DecryptionMailboxState
    DecryptionTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:decryptionEnv] -->
```juvix extract-module-statements
module decryption_environment_example;

decryptionEnv : DecryptionEnv :=
    mkEngineEnv@{
      localState := unit;
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:decryptionEnv] -->

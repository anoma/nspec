---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- encryption
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.encryption_environment;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.encryption_overview open;
    ```

# Encryption Engine Environment

## Overview

The Encryption Engine is stateless in terms of local state since it relies on external information (like the `reads_for` relationships) and does not maintain any internal state between requests.

## Mailbox States

The Encryption Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias EncryptionMailboxState := Unit;
```

## Local State

We can define the local state as `Unit` since the engine is stateless.

```juvix
syntax alias EncryptionLocalState := Unit;
```

## Timer Handles

The Encryption Engine does not require timers. We define the timer handle type as Unit.

```juvix
syntax alias EncryptionTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
EncryptionEnvironment : Type := EngineEnvironment
  EncryptionLocalState
  EncryptionMsg
  EncryptionMailboxState
  EncryptionTimerHandle;
```
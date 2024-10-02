---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- decryption
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.decryption_environment;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.decryption_overview open;
    ```

# Decryption Engine Environment

## Overview

Each Decryption Engine instance is associated with a specific identity and handles decryption requests for that identity.

## Mailbox States

The Decryption Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias DecryptionMailboxState := Unit;
```

## Local State

The local state of a Decryption Engine instance includes the identity's decryption capabilities and any necessary decryption keys or handles.

```juvix
type DecryptionLocalState := mkDecryptionLocalState {
  identity : ExternalIdentity;
  backend : IDBackend;
  decryptionKey : DecryptionKey;
};
```

## Timer Handles

The Decryption Engine does not require timers. We define the timer handle type as Unit.

```juvix
syntax alias DecryptionTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
DecryptionEnvironment : Type := EngineEnvironment
  DecryptionLocalState
  DecryptionMsg
  DecryptionMailboxState
  DecryptionTimerHandle;
```
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
    import arch.system.identity.identity open using {Decryptor; mkDecryptor};
    ```

# Decryption Environment

## Overview

Each Decryption Engine instance is associated with a specific identity and
handles decryption requests for that identity. The environment maintains the
necessary state for decryption operations.

## Mailbox states

The Decryption Engine does not require complex mailbox states. We define the
mailbox state as `Unit`.

```juvix
syntax alias DecryptionMailboxState := Unit;
```

## Local state

The local state of a Decryption Engine instance includes the identity's
decryption capabilities.

```juvix
type DecryptionLocalState := mkDecryptionLocalState {
  decryptor : Decryptor Backend Plaintext Ciphertext;
  backend : Backend;
};
```

## Timer Handle

```juvix
syntax alias DecryptionTimerHandle := Unit;
```

The Decryption Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

## Environment summary

```juvix
DecryptionEnvironment : Type := EngineEnvironment
  DecryptionLocalState
  DecryptionMailboxState
  DecryptionTimerHandle;
```

## Example of a `Decryption` environment

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module decryption_environment_example;

decryptionEnvironmentExample : DecryptionEnvironment :=
    mkEngineEnvironment@{
      name := "decryption";
      localState := mkDecryptionLocalState@{
        decryptor := mkDecryptor@{
          decrypt := \{_ x := some x};
        };
        backend := BackendLocalMemory;
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:environment-example] -->

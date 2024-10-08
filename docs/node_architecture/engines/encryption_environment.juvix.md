---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-family
tags:
- encryption
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.encryption_environment;

    import prelude open;
    import system_architecture.identity.identity open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.identity_types open;
    import node_architecture.engines.encryption_overview open;
    ```

# Encryption Environment

## Overview

The Encryption Engine is stateless and does not maintain any internal state between requests. It relies on external information (like the `reads_for` relationships) for its operations.

## Mailbox states

The Encryption Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias EncryptionMailboxState := Unit;
```

## Local state

The local state of a Encryption Engine instance includes the identity's encryption capabilities.

```juvix
type EncryptionLocalState := mkEncryptionLocalState {
  encryptor : Encryptor ByteString Backend ByteString ByteString;
  backend : Backend;
};
```

## Timer Handle

```juvix
syntax alias EncryptionTimerHandle := Unit;
```

The Encryption Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
EncryptionEnvironment : Type := EngineEnvironment 
  EncryptionLocalState 
  EncryptionMsg 
  EncryptionMailboxState 
  EncryptionTimerHandle;
```

## Example of an `Encryption` environment

```juvix extract-module-statements
module encryption_environment_example;

encryptionEnvironmentExample : EncryptionEnvironment :=
    mkEngineEnvironment@{
      name := Left "encryption";
      localState := mkEncryptionLocalState@{
        encryptor := mkEncryptor@{
          encrypt := \{_ x := x};
          encryptorHash := mkHASH@{
            ordKey := mkOrdkey@{
                compare := Ord.cmp
            };
            hash := \{x := 0};
          };
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

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

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.encryption_environment;

    import prelude open;
    import node_architecture.engines.encryption_overview open;
    import node_architecture.identity_types open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identities open;
    import node_architecture.types.messages open;
    import system_architecture.identity.identity open hiding {ExternalIdentity};
    ```

# `Encryption` Engine Environment

## Overview

The `Encryption` Engine is stateless and does not maintain any internal state
between requests. It relies on external information (like the `reads_for`
relationships) for its operations.

## Mailbox states

The `Encryption` Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias EncryptionMailboxState := Unit;
```

## Local state

The local state of an `Encryption` Engine instance includes the identity's
encryption capabilities, the address of an associated `ReadsFor` engine, and a
specific backend. It also contains a map to a list of pending requests which
require `ReadsFor` information which is requested from the associated `ReadsFor`
engine.

```juvix
type EncryptionLocalState := mkEncryptionLocalState {
  encryptor : Set ReadsForEvidence -> ExternalIdentity -> Encryptor ByteString Backend Plaintext Ciphertext;
  backend : Backend;
  readsForEngineAddress : EngineID;
  pendingRequests : Map ExternalIdentity (List (Pair EngineID Plaintext));
};
```

## Timer Handle

```juvix
syntax alias EncryptionTimerHandle := Unit;
```

The Encryption Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

## Environment summary

```juvix
EncryptionEnvironment : Type := EngineEnvironment
  EncryptionLocalState
  EncryptionMailboxState
  EncryptionTimerHandle;
```

## Example of an `Encryption` environment

```juvix extract-module-statements
module encryption_environment_example;

encryptionEnvironmentExample : EncryptionEnvironment :=
    mkEngineEnvironment@{
      name := "encryption";
      localState := mkEncryptionLocalState@{
        encryptor := \{_ _ := mkEncryptor@{
          encrypt := \{_ x := x};
          encryptorHash := mkHASH@{
            ordKey := mkOrdkey@{
                compare := Ord.cmp
            };
            hash := \{x := 0};
          };
        }};
        backend := BackendLocalMemory;
        readsForEngineAddress := mkPair none (some "Blah");
        pendingRequests := Map.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```

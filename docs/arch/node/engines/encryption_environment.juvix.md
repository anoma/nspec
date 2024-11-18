---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- encryption
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.encryption_environment;

    import prelude open;
    import arch.node.engines.encryption_messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
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
type EncryptionLocalState := mkEncryptionLocalState@{
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

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module encryption_environment_example;

encryptionEnvironmentExample : EncryptionEnvironment :=
    mkEngineEnvironment@{
      node := Curve25519PubKey "0xabcd1234";
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
<!-- --8<-- [end:environment-example] -->

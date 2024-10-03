---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-family
tags:
- decryption
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.decryption_environment;

    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.decryption_overview open;
    ```

# Decryption Environment

## Overview

Each Decryption Engine instance is associated with a specific identity and handles decryption requests for that identity. The environment maintains the necessary state for decryption operations.

## Mailbox states

The Decryption Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias DecryptionMailboxState := Unit;
```

## Local state

The local state of a Decryption Engine instance includes the identity's decryption capabilities and any necessary decryption keys or handles.

```juvix
type DecryptionLocalState := mkDecryptionLocalState {
  identity : ExternalIdentity;
  backend : IDBackend;
  decryptionKey : DecryptionKey;
};
```

## Timer Handle

```juvix
syntax alias DecryptionTimerHandle := Unit;
```

The Decryption Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
DecryptionEnvironment : Type := EngineEnvironment 
  DecryptionLocalState 
  DecryptionMsg 
  DecryptionMailboxState 
  DecryptionTimerHandle;
```

## Example of a `Decryption` environment

```juvix extract-module-statements
module decryption_environment_example;

axiom dummyExternalIdentity : ExternalIdentity;
axiom dummyIDBackend : IDBackend;
axiom dummyDecryptionKey : DecryptionKey;

decryptionEnvironmentExample : DecryptionEnvironment :=
    mkEngineEnvironment@{
      name := Left "decryption";
      localState := mkDecryptionLocalState@{
        identity := dummyExternalIdentity;
        backend := dummyIDBackend;
        decryptionKey := dummyDecryptionKey
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```

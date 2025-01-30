---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity
  - engine
  - naming
  - environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.naming_environment;

    import prelude open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.naming_messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Naming Environment

## Overview

The Naming Engine maintains the state necessary for managing associations between `IdentityName`s and `ExternalIdentity`s, including storing evidence submitted by clients.

??? quote "Auxiliary Juvix code"

    ```juvix
    axiom verifyEvidence : IdentityNameEvidence -> Bool;
    ```

## Mailbox states

The Naming Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `NamingMailboxState`

```juvix
syntax alias NamingMailboxState := Unit;
```

## Local state

The local state of the Naming Engine includes the evidence for name associations.

### `NamingLocalState`

```juvix
type NamingLocalState := mkNamingLocalState@{
  evidenceStore : Set IdentityNameEvidence;
};
```

???+ quote "Arguments"

    `evidenceStore`:
    : The pool of evidence which the engine uses for identity verification.

## Timer Handle

The Naming Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

### `NamingTimerHandle`

```juvix
syntax alias NamingTimerHandle := Unit;
```

## The Naming Environment

### `NamingEnv`

```juvix
NamingEnv : Type :=
  EngineEnv
    NamingLocalState
    NamingMailboxState
    NamingTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:namingEnv] -->
```juvix extract-module-statements
module naming_environment_example;

namingEnv : NamingEnv :=
    mkEngineEnv@{
      localState := mkNamingLocalState@{
        evidenceStore := Set.empty;
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:namingEnv] -->
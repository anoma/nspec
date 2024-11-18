---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- naming
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.naming_environment;

    import prelude open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.naming_messages open;
    ```

# Naming Environment

## Overview

The Naming Engine maintains the state necessary for managing associations between `IdentityName`s and `ExternalIdentity`s, including storing evidence submitted by clients.

## Mailbox states

The Naming Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias NamingMailboxState := Unit;
```

## Local state

The local state of the Naming Engine includes the evidence for name associations.

```juvix
type NamingLocalState := mkNamingLocalState@{
  evidenceStore : Set IdentityNameEvidence;
  verifyEvidence : IdentityNameEvidence -> Bool;
};
```

## Timer Handle

```juvix
syntax alias NamingTimerHandle := Unit;
```

The Naming Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
NamingEnvironment : Type := EngineEnvironment
  NamingLocalState
  NamingMailboxState
  NamingTimerHandle;
```

## Example of a `Naming` environment

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module naming_environment_example;

namingEnvironmentExample : NamingEnvironment :=
    mkEngineEnvironment@{
      node := Curve25519PubKey "0xabcd1234";
      name := "naming";
      localState := mkNamingLocalState@{
        evidenceStore := Set.empty;
        verifyEvidence := \{ _ := true }
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:environment-example] -->

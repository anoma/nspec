---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- naming
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.naming_environment;
    import prelude open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.naming_overview open;
    ```
    
# Naming Engine Environment

## Overview

The Naming Engine maintains the state necessary for managing associations between `IdentityName`s and `ExternalIdentity`s, including storing evidence submitted by clients.

## Mailbox States

The Naming Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias NamingMailboxState := Unit;
```

## Local State

The local state of the Naming Engine includes the evidence for name associations.

```juvix
type NamingLocalState := mkNamingLocalState {
  evidenceStore : Set IdentityNameEvidence;
};
```

## Timer Handles

The Naming Engine does not require timers. We define the timer handle type as Unit.

```juvix
syntax alias NamingTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
NamingEnvironment : Type := EngineEnvironment
  NamingLocalState
  NamingMsg
  NamingMailboxState
  NamingTimerHandle;
```
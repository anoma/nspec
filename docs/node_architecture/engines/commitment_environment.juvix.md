---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- commitment
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.commitment_environment;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.commitment_overview open;
    ```

# Commitment Engine Environment

## Overview

Each Commitment Engine instance is associated with a specific identity and handles commitment (signature) requests for that identity.

## Mailbox States

The Commitment Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias CommitmentMailboxState := Unit;
```

## Local State

The local state of a Commitment Engine instance includes the identity's signing capabilities and any necessary signing keys or handles.

```juvix
type CommitmentLocalState := mkCommitmentLocalState {
  identity : ExternalIdentity;
  backend : IDBackend;
  signingKey : SigningKey;
};
```

## Timer Handles

The Commitment Engine does not require timers. We define the timer handle type as Unit.

```juvix
syntax alias CommitmentTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
CommitmentEnvironment : Type := EngineEnvironment
  CommitmentLocalState
  CommitmentMsg
  CommitmentMailboxState
  CommitmentTimerHandle;
```

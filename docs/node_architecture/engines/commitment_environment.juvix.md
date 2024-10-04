---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-family
tags:
- commitment
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.commitment_environment;

    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.commitment_overview open;
    ```

# Commitment Environment

## Overview

The Commitment Engine environment maintains the state necessary for generating commitments (signatures) for a specific identity. It includes the identity's signing capabilities and any necessary signing keys or handles.

## Mailbox states

The Commitment Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias CommitmentMailboxState := Unit;
```

## Local state

The local state of a Commitment Engine instance includes the identity's signing capabilities and any necessary signing keys or handles.

```juvix
type CommitmentLocalState := mkCommitmentLocalState {
  identity : ExternalIdentity;
  backend : Backend;
  signingKey : SigningKey;
};
```

## Timer Handle

```juvix
syntax alias CommitmentTimerHandle := Unit;
```

The Commitment Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
CommitmentEnvironment : Type := EngineEnvironment 
  CommitmentLocalState 
  CommitmentMsg 
  CommitmentMailboxState 
  CommitmentTimerHandle;
```

## Example of a `Commitment` environment

```juvix extract-module-statements
module commitment_environment_example;

axiom dummyExternalIdentity : ExternalIdentity;
axiom dummyIDBackend : Backend;
axiom dummySigningKey : SigningKey;

commitmentEnvironmentExample : CommitmentEnvironment :=
    mkEngineEnvironment@{
      name := Left "commitment";
      localState := mkCommitmentLocalState@{
        identity := dummyExternalIdentity;
        backend := dummyIDBackend;
        signingKey := dummySigningKey
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```

---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- commitment
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.commitment_environment;
    import prelude open;
    import arch.system.identity.identity open using {Signer; mkSigner};
    import arch.node.engines.commitment_messages open;
    import arch.node.types.crypto open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Commitment Environment

## Overview

The Commitment Engine environment maintains the state necessary for generating
commitments (signatures) for a specific identity. It includes the identity's
signing capabilities and any necessary signing keys or handles.

## Mailbox states

The Commitment Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `CommitmentMailboxState`

```juvix
syntax alias CommitmentMailboxState := Unit;
```

## Local state

The local state of a Commitment Engine instance includes the identity's signing capabilities.

### `CommitmentLocalState`

```juvix
type CommitmentLocalState := mkCommitmentLocalState {
  signer : Signer Backend Signable Commitment;
  backend : Backend;
};
```

???+ quote "Arguments"

    `signer`:
    : The signer for the identity.

    `backend`:
    : The backend to use for signing.

## Timer Handle

The Commitment Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

### `CommitmentTimerHandle`

```juvix
syntax alias CommitmentTimerHandle := Unit;
```

## The Commitment Environment

### `CommitmentEnvironment`

```juvix
CommitmentEnvironment : Type :=
  EngineEnvironment
    CommitmentLocalState
    CommitmentMailboxState
    CommitmentTimerHandle;
```

### Instantiation

<!-- --8<-- [start:commitmentEnvironment] -->
```juvix extract-module-statements
module commitment_environment_example;

axiom dummyExternalIdentity : ExternalIdentity;
axiom dummyIDBackend : Backend;
axiom dummySigningKey : SigningKey;

commitmentEnvironment : CommitmentEnvironment :=
    mkEngineEnvironment@{
      name := "commitment";
      localState := mkCommitmentLocalState@{
        signer := mkSigner@{
          sign := \{_ x := Ed25519Signature};
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
<!-- --8<-- [end:commitmentEnvironment] -->

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

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.commitment_environment;
    import prelude open;
    import system_architecture.identity.identity open using {Signer; mkSigner};
    import node_architecture.engines.commitment_overview open;

    import node_architecture.types.crypto open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identities open;
    import node_architecture.types.messages open;
    ```

# Commitment Environment

## Overview

The Commitment Engine environment maintains the state necessary for generating
commitments (signatures) for a specific identity. It includes the identity's
signing capabilities and any necessary signing keys or handles.

## Mailbox states

The Commitment Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias CommitmentMailboxState := Unit;
```

## Local state

The local state of a Commitment Engine instance includes the identity's signing capabilities.

```juvix
type CommitmentLocalState := mkCommitmentLocalState {
  signer : Signer Backend Signable Commitment;
  backend : Backend;
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

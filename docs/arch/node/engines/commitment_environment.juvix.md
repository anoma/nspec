---
icon: octicons/container-24
search:
  exclude: false
tags:
- node-architecture
- identity
- engine
- commitment
- environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.commitment_environment;
    import prelude open;
    import arch.node.engines.commitment_messages open;
    import arch.node.types.crypto open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Commitment Environment

---

## Overview

The Commitment Engine environment maintains the state necessary for generating
commitments (signatures) for a specific identity. It includes the identity's
signing capabilities and any necessary signing keys or handles.

---

## Mailbox states

The Commitment Engine does not require complex mailbox states. We define the
mailbox state as `Unit`.

---

### `CommitmentMailboxState`

```juvix
syntax alias CommitmentMailboxState := Unit;
```

---

## Local state

The Commitment engine is statless.

---

### `CommitmentLocalState`

```juvix
syntax alias CommitmentLocalState := Unit;
```

---

## Timer Handle

The Commitment Engine does not require a timer handle type. Therefore, we define
the timer handle type as `Unit`.

---

### `CommitmentTimerHandle`

```juvix
syntax alias CommitmentTimerHandle := Unit;
```

## The Commitment Environment

---

### `CommitmentEnv`

```juvix
CommitmentEnv : Type :=
  EngineEnv
    CommitmentLocalState
    CommitmentMailboxState
    CommitmentTimerHandle
    Anoma.Msg;
```

---

### Instantiation

<!-- --8<-- [start:commitmentEnv] -->
```juvix extract-module-statements
module commitment_environment_example;

axiom dummyExternalIdentity : ExternalIdentity;
axiom dummyIDBackend : Backend;
axiom dummySigningKey : SigningKey;

commitmentEnv : CommitmentEnv :=
    mkEngineEnv@{
      localState := unit;
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:commitmentEnv] -->

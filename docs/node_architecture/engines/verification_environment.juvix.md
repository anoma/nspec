---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- verification
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.verification_environment;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.verification_overview open;
    ```

# Verification Engine Environment

## Overview

The Verification Engine is stateless in terms of local state since it relies on external information (like the `signs_for` relationships) and does not maintain any internal state between requests.

## Mailbox States

The Verification Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias VerificationMailboxState := Unit;
```

## Local State

We can define the local state as Unit since the engine is stateless.

```juvix
syntax alias VerificationLocalState := Unit;
```

## Timer Handles

The Verification Engine does not require timers. We define the timer handle type as Unit.

```juvix
syntax alias VerificationTimerHandle := Unit;
```

## Environment Summary

We define the environment type as:

```juvix
VerificationEnvironment : Type := EngineEnvironment
  VerificationLocalState
  VerificationMsg
  VerificationMailboxState
  VerificationTimerHandle;
```

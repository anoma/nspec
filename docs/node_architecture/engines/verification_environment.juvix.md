---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-family
tags:
- verification
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.verification_environment;

    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.identity_types open;
    import node_architecture.engines.verification_overview open;
    ```

# Verification Environment

## Overview

The Verification Engine is stateless and does not maintain any internal state between requests. It relies on external information (like the `signs_for` relationships) for its operations.

## Mailbox states

The Verification Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias VerificationMailboxState := Unit;
```

## Local state

The Verification Engine is stateless, so we define the local state as `Unit`.

```juvix
syntax alias VerificationLocalState := Unit;
```

## Timer Handle

```juvix
syntax alias VerificationTimerHandle := Unit;
```

The Verification Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
VerificationEnvironment : Type := EngineEnvironment 
  VerificationLocalState
  VerificationMailboxState 
  VerificationTimerHandle;
```

## Example of a `Verification` environment

```juvix extract-module-statements
module verification_environment_example;

verificationEnvironmentExample : VerificationEnvironment :=
    mkEngineEnvironment@{
      name := Left "verification";
      localState := unit;
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```

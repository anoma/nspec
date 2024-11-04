---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- verification
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.verification_environment;

    import prelude open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
    import arch.node.types.messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.engines.verification_messages open;
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

The local state of a Verification Engine instance includes the identity's verification capabilities, the address of an associated `SignsFor` engine, and a specific backend. It also contains a map to a list of pending requests which require `SignsFor` information which is requested from the associated `SignsFor` engine.

```juvix
type VerificationLocalState := mkVerificationLocalState {
  verifier : Set SignsForEvidence -> ExternalIdentity -> Verifier ByteString Backend Signable Commitment;
  backend : Backend;
  signsForEngineAddress : EngineID;
  pendingRequests : Map ExternalIdentity (List (Pair EngineID (Pair Signable Commitment)));
};
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

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module verification_environment_example;

verificationEnvironmentExample : VerificationEnvironment :=
    mkEngineEnvironment@{
      name := "verification";
      localState := mkVerificationLocalState@{
        verifier := \{_ _ := mkVerifier@{
          verify := \{_ _ _ := true};
          verifierHash := mkHASH@{
            ordKey := mkOrdkey@{
                compare := Ord.cmp
            };
            hash := \{x := 0};
          };
        }};
        backend := BackendLocalMemory;
        signsForEngineAddress := mkPair none (some "Blah");
        pendingRequests := Map.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:environment-example] -->

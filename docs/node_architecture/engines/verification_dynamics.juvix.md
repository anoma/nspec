---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- verification
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.verification_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.verification_environment open;
    import node_architecture.engines.verification_overview open;
    import node_architecture.types.identity_types open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# Verification Engine Dynamics

## Overview

The dynamics of the Verification Engine define how it processes incoming verification requests and produces the corresponding responses.

## Action Labels

```juvix
type VerificationActionLabel :=
  | DoVerify VerifyRequest;
```

## Matchable Arguments

```juvix
type VerificationMatchableArgument :=
  | ArgVerify VerifyRequest;
```

## Precomputation Results

```juvix
syntax alias VerificationPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
VerificationGuard : Type :=
  Guard
    VerificationLocalState
    VerificationMsg
    VerificationMailboxState
    VerificationTimerHandle
    VerificationMatchableArgument
    VerificationActionLabel
    VerificationPrecomputation;
```

### `verifyGuard`

```juvix
verifyGuard
  (t : TimestampedTrigger VerificationMsg VerificationTimerHandle)
  (env : VerificationEnvironment)
  : Maybe (GuardOutput VerificationMatchableArgument VerificationActionLabel VerificationPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgVerifyRequest request) := just (mkGuardOutput@{
        args := [ArgVerify request];
        label := DoVerify request;
        other := unit
      })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and produces the verification response.

```juvix
VerificationActionInput : Type :=
  ActionInput
    VerificationLocalState
    VerificationMsg
    VerificationMailboxState
    VerificationTimerHandle
    VerificationMatchableArgument
    VerificationActionLabel
    VerificationPrecomputation;

VerificationActionEffect : Type :=
  ActionEffect
    VerificationLocalState
    VerificationMsg
    VerificationMailboxState
    VerificationTimerHandle
    VerificationMatchableArgument
    VerificationActionLabel
    VerificationPrecomputation;
```

### `verificationAction`

```juvix
-- Not yet implemented
axiom verifyCommitment : ExternalIdentity -> Commitment -> ByteString -> Bool;
axiom resolveSignsFor : ExternalIdentity -> ExternalIdentity;

verificationAction
  (input : VerificationActionInput)
  : VerificationActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
  in
  case GuardOutput.label out of {
    | DoVerify request := let
        -- Placeholder for checking and possibly updating the external identity using SignsFor relationships
        finalIdentity := case VerifyRequest.useSignsFor request of {
          | true := resolveSignsFor (VerifyRequest.externalIdentity request)
          | false := VerifyRequest.externalIdentity request
        };
        isValid := verifyCommitment finalIdentity
                                   (VerifyRequest.commitment request)
                                   (VerifyRequest.data request);
        responseMsgVer := MsgVerifyResponse (mkVerifyResponse@{
          result := isValid;
          error := nothing
        });
        senderVer := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetVer := case senderVer of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetVer;
            mailbox := nothing;
            message := Anoma.MsgVerification responseMsgVer
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
verificationConflictSolver : Set VerificationMatchableArgument -> List (Set VerificationMatchableArgument)
  | _ := [];
```
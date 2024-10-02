---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- commitment
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.commitment_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.commitment_environment open;
    import node_architecture.engines.commitment_overview open;
    import node_architecture.types.identity_types open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# Commitment Engine Dynamics

## Overview

The dynamics of the Commitment Engine define how it processes incoming commitment requests and produces the corresponding responses.

## Action Labels

```juvix
type CommitmentActionLabel :=
  | DoCommit CommitRequest;
```

## Matchable Arguments

```juvix
type CommitmentMatchableArgument :=
  | ArgCommit CommitRequest;
```

## Precomputation Results

```juvix
syntax alias CommitmentPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
CommitmentGuard : Type :=
  Guard
    CommitmentLocalState
    CommitmentMsg
    CommitmentMailboxState
    CommitmentTimerHandle
    CommitmentMatchableArgument
    CommitmentActionLabel
    CommitmentPrecomputation;
```

### `commitGuard`

```juvix
commitGuard
  (t : TimestampedTrigger CommitmentMsg CommitmentTimerHandle)
  (env : CommitmentEnvironment)
  : Maybe (GuardOutput CommitmentMatchableArgument CommitmentActionLabel CommitmentPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgCommitRequest request) := just (mkGuardOutput@{
        args := [ArgCommit request];
        label := DoCommit request;
        other := unit
      })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and updates the environment accordingly.

```juvix
CommitmentActionInput : Type :=
  ActionInput
    CommitmentLocalState
    CommitmentMsg
    CommitmentMailboxState
    CommitmentTimerHandle
    CommitmentMatchableArgument
    CommitmentActionLabel
    CommitmentPrecomputation;

CommitmentActionEffect : Type :=
  ActionEffect
    CommitmentLocalState
    CommitmentMsg
    CommitmentMailboxState
    CommitmentTimerHandle
    CommitmentMatchableArgument
    CommitmentActionLabel
    CommitmentPrecomputation;
```

### `commitmentAction`

```juvix
-- Not yet implemented
axiom signData : SigningKey -> Signable -> Either String Commitment;

commitmentAction
  (input : CommitmentActionInput)
  : CommitmentActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoCommit request := let
        signedData := signData (CommitmentLocalState.signingKey localState) (CommitRequest.data request);
        responseMsgCom := case signedData of {
          | Left errorMsg := MsgCommitResponse (mkCommitResponse@{
              commitment := emptyCommitment;
              error := just errorMsg
            })
          | Right commitment' := MsgCommitResponse (mkCommitResponse@{
              commitment := commitment';
              error := nothing
            })
        };
        senderCom := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetCom := case senderCom of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetCom;
            mailbox := nothing;
            message := Anoma.MsgCommitment responseMsgCom
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
commitmentConflictSolver : Set CommitmentMatchableArgument -> List (Set CommitmentMatchableArgument)
  | _ := [];
```


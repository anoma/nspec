---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- signs_for
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.signs_for_dynamics;
    import prelude open;
    import Stdlib.Data.List.Base open;
    import Data.Set.AVL open;
    import Stdlib.Trait.Ord open;
    import Stdlib.Data.Bool.Base open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.signs_for_environment open;
    import node_architecture.engines.signs_for_overview open;
    import node_architecture.types.anoma_message as Anoma;
    ```
    
# Signs For Engine Dynamics

## Overview

The dynamics of the Signs For Engine define how it processes incoming messages and updates its state accordingly.

## Action Labels

```juvix
type SignsForActionLabel :=
  | DoSignsForQuery SignsForRequest
  | DoSubmitEvidence SubmitSignsForEvidenceRequest
  | DoQueryEvidence QuerySignsForEvidenceRequest;
```

## Matchable Arguments

```juvix
type SignsForMatchableArgument :=
  | ArgSignsForQuery SignsForRequest
  | ArgSubmitEvidence SubmitSignsForEvidenceRequest
  | ArgQueryEvidence QuerySignsForEvidenceRequest;
```

## Precomputation Results

```juvix
syntax alias SignsForPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
SignsForGuard : Type :=
  Guard
    SignsForLocalState
    SignsForMsg
    SignsForMailboxState
    SignsForTimerHandle
    SignsForMatchableArgument
    SignsForActionLabel
    SignsForPrecomputation;
```

### `signsForQueryGuard`

```juvix
signsForQueryGuard
  (t : TimestampedTrigger SignsForMsg SignsForTimerHandle)
  (env : SignsForEnvironment)
  : Maybe (GuardOutput SignsForMatchableArgument SignsForActionLabel SignsForPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgSignsForRequest request) := just (mkGuardOutput@{
        args := [ArgSignsForQuery request];
        label := DoSignsForQuery request;
        other := unit
      })
    | _ := nothing
  };
```

### `submitEvidenceGuard`

```juvix
submitEvidenceGuard
  (t : TimestampedTrigger SignsForMsg SignsForTimerHandle)
  (env : SignsForEnvironment)
  : Maybe (GuardOutput SignsForMatchableArgument SignsForActionLabel SignsForPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgSubmitSignsForEvidenceRequest request) := just (mkGuardOutput@{
        args := [ArgSubmitEvidence request];
        label := DoSubmitEvidence request;
        other := unit
      })
    | _ := nothing
  };
```

### `queryEvidenceGuard`

```juvix
queryEvidenceGuard
  (t : TimestampedTrigger SignsForMsg SignsForTimerHandle)
  (env : SignsForEnvironment)
  : Maybe (GuardOutput SignsForMatchableArgument SignsForActionLabel SignsForPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgQuerySignsForEvidenceRequest request) := just (mkGuardOutput@{
        args := [ArgQueryEvidence request];
        label := DoQueryEvidence request;
        other := unit
      })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and updates the environment accordingly.

```juvix
SignsForActionInput : Type :=
  ActionInput
    SignsForLocalState
    SignsForMsg
    SignsForMailboxState
    SignsForTimerHandle
    SignsForMatchableArgument
    SignsForActionLabel
    SignsForPrecomputation;

SignsForActionEffect : Type :=
  ActionEffect
    SignsForLocalState
    SignsForMsg
    SignsForMailboxState
    SignsForTimerHandle
    SignsForMatchableArgument
    SignsForActionLabel
    SignsForPrecomputation;
```

### `signsForAction`

```juvix
signsForAction
  (input : SignsForActionInput)
  : SignsForActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoSignsForQuery request := let
        hasEvidence := elem \{a b := a && b} true (map \{evidence :=
          isEQ (Ord.cmp (SignsForEvidence.fromIdentity evidence) (SignsForRequest.externalIdentityA request)) &&
          isEQ (Ord.cmp (SignsForEvidence.toIdentity evidence) (SignsForRequest.externalIdentityB request))
         } (toList (SignsForLocalState.evidenceStore localState)));
        responseMsgSF := MsgSignsForResponse (mkSignsForResponse@{
          signsFor := hasEvidence;
          error := nothing
        });
        senderSF := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetSF := case senderSF of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetSF;
            mailbox := nothing;
            message := Anoma.MsgSignsFor responseMsgSF
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoSubmitEvidence request := let
        newEvidenceStore := Set.insert (SubmitSignsForEvidenceRequest.evidence request) (SignsForLocalState.evidenceStore localState);
        newLocalStateSF := mkSignsForLocalState@{
          evidenceStore := newEvidenceStore
        };
        newEnvSF := env@EngineEnvironment{
          localState := newLocalStateSF
        };
        responseMsgSubmit := MsgSubmitSignsForEvidenceResponse (mkSubmitSignsForEvidenceResponse@{
          error := nothing
        });
        senderSubmit := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetSubmit := case senderSubmit of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvSF;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetSubmit;
            mailbox := nothing;
            message := Anoma.MsgSignsFor responseMsgSubmit
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoQueryEvidence request := let
        relevantEvidence := AVLfilter \{evidence :=
          isEQ (Ord.cmp (SignsForEvidence.fromIdentity evidence) (QuerySignsForEvidenceRequest.externalIdentity request)) ||
          isEQ (Ord.cmp (SignsForEvidence.toIdentity evidence) (QuerySignsForEvidenceRequest.externalIdentity request))
         } (SignsForLocalState.evidenceStore localState);
        responseMsgQuery := MsgQuerySignsForEvidenceResponse (mkQuerySignsForEvidenceResponse@{
          evidence := relevantEvidence;
          error := nothing
        });
        senderQuery := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetQuery := case senderQuery of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetQuery;
            mailbox := nothing;
            message := Anoma.MsgSignsFor responseMsgQuery
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
signsForConflictSolver : Set SignsForMatchableArgument -> List (Set SignsForMatchableArgument)
  | _ := [];
```
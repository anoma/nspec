---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- reads_for
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.reads_for_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import Data.Set.AVL open;
    import Stdlib.Data.List.Base open;
    import Stdlib.Trait.Ord open;
    import Stdlib.Data.Bool.Base open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.reads_for_overview open;
    import node_architecture.engines.reads_for_environment open;
    import node_architecture.types.anoma_message as Anoma;
    ```
    
# Reads For Engine Dynamics

## Overview

The dynamics of the Reads For Engine define how it processes incoming messages and updates its state accordingly.

## Action Labels

```juvix
type ReadsForActionLabel :=
  | DoReadsForQuery ReadsForRequest
  | DoSubmitEvidence SubmitReadsForEvidenceRequest
  | DoQueryEvidence QueryReadsForEvidenceRequest;
```

## Matchable Arguments

```juvix
type ReadsForMatchableArgument :=
  | ArgReadsForQuery ReadsForRequest
  | ArgSubmitEvidence SubmitReadsForEvidenceRequest
  | ArgQueryEvidence QueryReadsForEvidenceRequest;
```

## Precomputation Results

```juvix
syntax alias ReadsForPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
ReadsForGuard : Type :=
  Guard
    ReadsForLocalState
    ReadsForMsg
    ReadsForMailboxState
    ReadsForTimerHandle
    ReadsForMatchableArgument
    ReadsForActionLabel
    ReadsForPrecomputation;
```

### `readsForQueryGuard`

```juvix
readsForQueryGuard
  (t : TimestampedTrigger ReadsForMsg ReadsForTimerHandle)
  (env : ReadsForEnvironment)
  : Maybe (GuardOutput ReadsForMatchableArgument ReadsForActionLabel ReadsForPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgReadsForRequest request) := just (mkGuardOutput@{
        args := [ArgReadsForQuery request];
        label := DoReadsForQuery request;
        other := unit
      })
    | _ := nothing
  };
```

### `submitEvidenceGuard`

```juvix
submitEvidenceGuard
  (t : TimestampedTrigger ReadsForMsg ReadsForTimerHandle)
  (env : ReadsForEnvironment)
  : Maybe (GuardOutput ReadsForMatchableArgument ReadsForActionLabel ReadsForPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgSubmitReadsForEvidenceRequest request) := just (mkGuardOutput@{
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
  (t : TimestampedTrigger ReadsForMsg ReadsForTimerHandle)
  (env : ReadsForEnvironment)
  : Maybe (GuardOutput ReadsForMatchableArgument ReadsForActionLabel ReadsForPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgQueryReadsForEvidenceRequest request) := just (mkGuardOutput@{
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
ReadsForActionInput : Type :=
  ActionInput
    ReadsForLocalState
    ReadsForMsg
    ReadsForMailboxState
    ReadsForTimerHandle
    ReadsForMatchableArgument
    ReadsForActionLabel
    ReadsForPrecomputation;

ReadsForActionEffect : Type :=
  ActionEffect
    ReadsForLocalState
    ReadsForMsg
    ReadsForMailboxState
    ReadsForTimerHandle
    ReadsForMatchableArgument
    ReadsForActionLabel
    ReadsForPrecomputation;
```

### `readsForAction`

```juvix
readsForAction
  (input : ReadsForActionInput)
  : ReadsForActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoReadsForQuery request := let
        hasEvidence := elem \{a b := a && b} true (map \{ evidence :=
          isEQ (Ord.cmp (ReadsForEvidence.fromIdentity evidence) (ReadsForRequest.externalIdentityA request)) &&
          isEQ (Ord.cmp (ReadsForEvidence.toIdentity evidence) (ReadsForRequest.externalIdentityB request))
        } (toList (ReadsForLocalState.evidenceStore localState)));
        responseMsgRF := MsgReadsForResponse (mkReadsForResponse@{
          readsFor := hasEvidence;
          error := nothing
        });
        senderRF := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetRF := case senderRF of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetRF;
            mailbox := nothing;
            message := Anoma.MsgReadsFor responseMsgRF
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoSubmitEvidence request := let
        newEvidenceStore := Set.insert (SubmitReadsForEvidenceRequest.evidence request) (ReadsForLocalState.evidenceStore localState);
        newLocalStateRF := mkReadsForLocalState@{
          evidenceStore := newEvidenceStore
        };
        newEnvRF := env@EngineEnvironment{
          localState := newLocalStateRF
        };
        responseMsgSubmit := MsgSubmitReadsForEvidenceResponse (mkSubmitReadsForEvidenceResponse@{
          error := nothing
        });
        senderSubmit := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetSubmit := case senderSubmit of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvRF;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetSubmit;
            mailbox := nothing;
            message := Anoma.MsgReadsFor responseMsgSubmit
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoQueryEvidence request := let
        relevantEvidence := AVLfilter \{evidence :=
          isEQ (Ord.cmp (ReadsForEvidence.fromIdentity evidence) (QueryReadsForEvidenceRequest.externalIdentity request)) ||
          isEQ (Ord.cmp (ReadsForEvidence.toIdentity evidence) (QueryReadsForEvidenceRequest.externalIdentity request))
        } (ReadsForLocalState.evidenceStore localState);
        responseMsgQuery := MsgQueryReadsForEvidenceResponse (mkQueryReadsForEvidenceResponse@{
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
            message := Anoma.MsgReadsFor responseMsgQuery
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
readsForConflictSolver : Set ReadsForMatchableArgument -> List (Set ReadsForMatchableArgument)
  | _ := [];
```
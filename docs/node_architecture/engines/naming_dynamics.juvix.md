---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- naming
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.naming_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import Data.Set.AVL open;
    import Stdlib.Data.List.Base open;
    import Stdlib.Trait.Ord open;
    import Stdlib.Data.Bool.Base open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.naming_overview open;
    import node_architecture.engines.naming_environment open;
    import node_architecture.types.anoma_message as Anoma;
    ```
    
# Naming Engine Dynamics

## Overview

The dynamics of the Naming Engine define how it processes incoming messages and updates its state accordingly.

## Action Labels

```juvix
type NamingActionLabel :=
  | DoResolveName ResolveNameRequest
  | DoSubmitNameEvidence SubmitNameEvidenceRequest
  | DoQueryNameEvidence QueryNameEvidenceRequest;
```

## Matchable Arguments

```juvix
type NamingMatchableArgument :=
  | ArgResolveName ResolveNameRequest
  | ArgSubmitNameEvidence SubmitNameEvidenceRequest
  | ArgQueryNameEvidence QueryNameEvidenceRequest;
```

## Precomputation Results

```juvix
syntax alias NamingPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
NamingGuard : Type :=
  Guard
    NamingLocalState
    NamingMsg
    NamingMailboxState
    NamingTimerHandle
    NamingMatchableArgument
    NamingActionLabel
    NamingPrecomputation;
```

### `resolveNameGuard`

```juvix
resolveNameGuard
  (t : TimestampedTrigger NamingMsg NamingTimerHandle)
  (env : NamingEnvironment)
  : Maybe (GuardOutput NamingMatchableArgument NamingActionLabel NamingPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgResolveNameRequest request) := just (mkGuardOutput@{
        args := [ArgResolveName request];
        label := DoResolveName request;
        other := unit
      })
    | _ := nothing
  };
```

### `submitNameEvidenceGuard`

```juvix
submitNameEvidenceGuard
  (t : TimestampedTrigger NamingMsg NamingTimerHandle)
  (env : NamingEnvironment)
  : Maybe (GuardOutput NamingMatchableArgument NamingActionLabel NamingPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgSubmitNameEvidenceRequest request) := just (mkGuardOutput@{
        args := [ArgSubmitNameEvidence request];
        label := DoSubmitNameEvidence request;
        other := unit
      })
    | _ := nothing
  };
```

### `queryNameEvidenceGuard`

```juvix
queryNameEvidenceGuard
  (t : TimestampedTrigger NamingMsg NamingTimerHandle)
  (env : NamingEnvironment)
  : Maybe (GuardOutput NamingMatchableArgument NamingActionLabel NamingPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgQueryNameEvidenceRequest request) := just (mkGuardOutput@{
        args := [ArgQueryNameEvidence request];
        label := DoQueryNameEvidence request;
        other := unit
      })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and updates the environment accordingly.

```juvix
NamingActionInput : Type :=
  ActionInput
    NamingLocalState
    NamingMsg
    NamingMailboxState
    NamingTimerHandle
    NamingMatchableArgument
    NamingActionLabel
    NamingPrecomputation;

NamingActionEffect : Type :=
  ActionEffect
    NamingLocalState
    NamingMsg
    NamingMailboxState
    NamingTimerHandle
    NamingMatchableArgument
    NamingActionLabel
    NamingPrecomputation;
```

### `namingAction`

```juvix
namingAction
  (input : NamingActionInput)
  : NamingActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoResolveName request := let
        matchingEvidence := AVLfilter \{evidence :=
          isEQ (Ord.cmp (IdentityNameEvidence.identityName evidence) (ResolveNameRequest.identityName request))
         } (NamingLocalState.evidenceStore localState);
        identities := fromList (map \{evidence :=
          IdentityNameEvidence.externalIdentity evidence
         } (toList matchingEvidence));
        responseMsgRes := MsgResolveNameResponse (mkResolveNameResponse@{
          externalIdentities := identities;
          error := nothing
        });
        senderRes := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetRes := case senderRes of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetRes;
            mailbox := nothing;
            message := Anoma.MsgNaming responseMsgRes
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoSubmitNameEvidence request := let
        evidence := SubmitNameEvidenceRequest.evidence request;
        alreadyExists := elem \{a b := a && b} true (map \{e :=
          isEQ (Ord.cmp e evidence)
         } (toList (NamingLocalState.evidenceStore localState)));
        newLocalStateName := case alreadyExists of { 
              | true := localState
              | false :=
          let newEvidenceStore := Set.insert evidence (NamingLocalState.evidenceStore localState);
          in mkNamingLocalState@{
            evidenceStore := newEvidenceStore
          }};
        newEnvName := env@EngineEnvironment{
          localState := newLocalStateName
        };
        responseMsgSubmit := MsgSubmitNameEvidenceResponse (mkSubmitNameEvidenceResponse@{
          error := case alreadyExists of { 
            | true := just "Evidence already exists" 
            | false := nothing
        }});
        senderSubmit := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetSubmit := case senderSubmit of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvName;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetSubmit;
            mailbox := nothing;
            message := Anoma.MsgNaming responseMsgSubmit
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoQueryNameEvidence request := let
        relevantEvidence := AVLfilter \{evidence :=
          isEQ (Ord.cmp (IdentityNameEvidence.externalIdentity evidence) (QueryNameEvidenceRequest.externalIdentity request))
         } (NamingLocalState.evidenceStore localState);
        responseMsgQuery := MsgQueryNameEvidenceResponse (mkQueryNameEvidenceResponse@{
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
            message := Anoma.MsgNaming responseMsgQuery
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
namingConflictSolver : Set NamingMatchableArgument -> List (Set NamingMatchableArgument)
  | _ := [];
```

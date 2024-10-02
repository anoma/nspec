---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- identity_management
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.identity_management_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.identity_management_overview open;
    import node_architecture.engines.identity_management_environment open;
    import node_architecture.types.anoma_message open;
    import node_architecture.types.identity_types open;
    ```
    
# Identity Management Engine Dynamics

## Overview

The dynamics of the Identity Management Engine define how it processes incoming messages (requests) and produces the corresponding responses and actions.

## Action Labels

```juvix
type IdentityManagementActionLabel :=
  | DoGenerateIdentity GenerateIdentityRequest
  | DoConnectIdentity ConnectIdentityRequest
  | DoDeleteIdentity DeleteIdentityRequest;
```

## Matchable Arguments

```juvix
type IdentityManagementMatchableArgument :=
  | ArgGenerateIdentity GenerateIdentityRequest
  | ArgConnectIdentity ConnectIdentityRequest
  | ArgDeleteIdentity DeleteIdentityRequest;
```

## Precomputation Results

```juvix
syntax alias IdentityManagementPrecomputation := Unit;
```

## Guards

We define guards that determine when certain actions are triggered based on incoming messages.

```juvix
IdentityManagementGuard : Type :=
  Guard
    IdentityManagementLocalState
    IdentityManagementMsg
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementMatchableArgument
    IdentityManagementActionLabel
    IdentityManagementPrecomputation;
```

### `generateIdentityGuard`

```juvix
generateIdentityGuard
  (t : TimestampedTrigger IdentityManagementMsg IdentityManagementTimerHandle)
  (env : IdentityManagementEnvironment)
  : Maybe (GuardOutput IdentityManagementMatchableArgument IdentityManagementActionLabel IdentityManagementPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgGenerateIdentityRequest request) :=
        just (mkGuardOutput@{
          args := [ArgGenerateIdentity request];
          label := DoGenerateIdentity request;
          other := unit
        })
    | _ := nothing
  };
```

### `connectIdentityGuard`

```juvix
connectIdentityGuard
  (t : TimestampedTrigger IdentityManagementMsg IdentityManagementTimerHandle)
  (env : IdentityManagementEnvironment)
  : Maybe (GuardOutput IdentityManagementMatchableArgument IdentityManagementActionLabel IdentityManagementPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgConnectIdentityRequest request) :=
        just (mkGuardOutput@{
          args := [ArgConnectIdentity request];
          label := DoConnectIdentity request;
          other := unit
        })
    | _ := nothing
  };
```

### `deleteIdentityGuard`

```juvix
deleteIdentityGuard
  (t : TimestampedTrigger IdentityManagementMsg IdentityManagementTimerHandle)
  (env : IdentityManagementEnvironment)
  : Maybe (GuardOutput IdentityManagementMatchableArgument IdentityManagementActionLabel IdentityManagementPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgDeleteIdentityRequest request) :=
        just (mkGuardOutput@{
          args := [ArgDeleteIdentity request];
          label := DoDeleteIdentity request;
          other := unit
        })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and updates the environment accordingly.

```juvix
IdentityManagementActionInput : Type :=
  ActionInput
    IdentityManagementLocalState
    IdentityManagementMsg
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementMatchableArgument
    IdentityManagementActionLabel
    IdentityManagementPrecomputation;

IdentityManagementActionEffect : Type :=
  ActionEffect
    IdentityManagementLocalState
    IdentityManagementMsg
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementMatchableArgument
    IdentityManagementActionLabel
    IdentityManagementPrecomputation;
```

### `identityManagementAction`

```juvix
-- Not yet implemented
axiom generateNewExternalIdentity : Params -> ExternalIdentity;

identityManagementAction
  (input : IdentityManagementActionInput)
  : IdentityManagementActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
  in
  case GuardOutput.label out of {
    | DoGenerateIdentity request := let
        -- Simulate identity generation (placeholder function)
        newIdentity := generateNewExternalIdentity (GenerateIdentityRequest.params request);
        identityInfo := mkIdentityInfo@{
          backend := GenerateIdentityRequest.backend request;
          capabilities := GenerateIdentityRequest.capabilities request;
          commitmentEngine := nothing; -- Placeholder for engine reference
          decryptionEngine := nothing; -- Placeholder for engine reference
        };
        updatedIdentities := Map.insert newIdentity identityInfo (IdentityManagementLocalState.identities (EngineEnvironment.localState env));
        newLocalState := mkIdentityManagementLocalState@{
          identities := updatedIdentities
        };
        newEnv := env@EngineEnvironment{
          localState := newLocalState
        };
        responseMsg := MsgGenerateIdentityResponse (mkGenerateIdentityResponse@{
          commitmentEngine := IdentityInfo.commitmentEngine identityInfo;
          decryptionEngine := IdentityInfo.decryptionEngine identityInfo;
          externalIdentity := newIdentity;
          error := nothing
        });
        sender := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        target := case sender of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnv;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := target;
            mailbox := nothing;
            message := MsgIdentityManagement responseMsg
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoConnectIdentity request := let
        identityInfo := mkIdentityInfo@{
          backend := ConnectIdentityRequest.backend request;
          capabilities := ConnectIdentityRequest.capabilities request;
          commitmentEngine := nothing; -- Placeholder
          decryptionEngine := nothing; -- Placeholder
        };
        updatedIdentities := Map.insert (ConnectIdentityRequest.externalIdentity request) identityInfo (IdentityManagementLocalState.identities (EngineEnvironment.localState env));
        newLocalState := mkIdentityManagementLocalState@{
          identities := updatedIdentities
        };
        newEnv := env@EngineEnvironment{
          localState := newLocalState
        };
        responseMsg := MsgConnectIdentityResponse (mkConnectIdentityResponse@{
          commitmentEngine := IdentityInfo.commitmentEngine identityInfo;
          decryptionEngine := IdentityInfo.decryptionEngine identityInfo;
          error := nothing
        });
        sender := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        target := case sender of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnv;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := target;
            mailbox := nothing;
            message := MsgIdentityManagement responseMsg
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoDeleteIdentity request := let
        updatedIdentities := Map.delete (DeleteIdentityRequest.externalIdentity request) (IdentityManagementLocalState.identities (EngineEnvironment.localState env));
        newLocalState := mkIdentityManagementLocalState@{
          identities := updatedIdentities
        };
        newEnv := env@EngineEnvironment{
          localState := newLocalState
        };
        responseMsg := MsgDeleteIdentityResponse (mkDeleteIdentityResponse@{
          error := nothing
        });
        sender := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        target := case sender of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnv;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := target;
            mailbox := nothing;
            message := MsgIdentityManagement responseMsg
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
identityManagementConflictSolver : Set IdentityManagementMatchableArgument -> List (Set IdentityManagementMatchableArgument)
  | _ := [];
``` 

## Identity Management Engine Family Summary

--8<-- "./docs/node_architecture/engines/ticker.juvix.md:ticker-engine-family"
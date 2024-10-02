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
axiom generateNewExternalIdentity : IDParams -> ExternalIdentity;

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
        newLocalStateGen := mkIdentityManagementLocalState@{
          identities := updatedIdentities
        };
        newEnvGen := env@EngineEnvironment{
          localState := newLocalStateGen
        };
        responseMsgGen := MsgGenerateIdentityResponse (mkGenerateIdentityResponse@{
          commitmentEngine := IdentityInfo.commitmentEngine identityInfo;
          decryptionEngine := IdentityInfo.decryptionEngine identityInfo;
          externalIdentity := newIdentity;
          error := nothing
        });
        senderGen := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetGen := case senderGen of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvGen;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetGen;
            mailbox := nothing;
            message := MsgIdentityManagement responseMsgGen
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
        newLocalStateConn := mkIdentityManagementLocalState@{
          identities := updatedIdentities
        };
        newEnvConn := env@EngineEnvironment{
          localState := newLocalStateConn
        };
        responseMsgConn := MsgConnectIdentityResponse (mkConnectIdentityResponse@{
          commitmentEngine := IdentityInfo.commitmentEngine identityInfo;
          decryptionEngine := IdentityInfo.decryptionEngine identityInfo;
          error := nothing
        });
        senderConn := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetConn := case senderConn of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvConn;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetConn;
            mailbox := nothing;
            message := MsgIdentityManagement responseMsgConn
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoDeleteIdentity request := let
        updatedIdentities := Map.delete (DeleteIdentityRequest.externalIdentity request) (IdentityManagementLocalState.identities (EngineEnvironment.localState env));
        newLocalStateDel := mkIdentityManagementLocalState@{
          identities := updatedIdentities
        };
        newEnvDel := env@EngineEnvironment{
          localState := newLocalStateDel
        };
        responseMsgDel := MsgDeleteIdentityResponse (mkDeleteIdentityResponse@{
          error := nothing
        });
        senderDel := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetDel := case senderDel of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvDel;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetDel;
            mailbox := nothing;
            message := MsgIdentityManagement responseMsgDel
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

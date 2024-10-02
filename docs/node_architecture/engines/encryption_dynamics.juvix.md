---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- encryption
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.encryption_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.encryption_environment open;
    import node_architecture.engines.encryption_overview open;
    import node_architecture.types.identity_types open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# Encryption Engine Dynamics

## Overview

The dynamics of the Encryption Engine define how it processes incoming encryption requests and produces the corresponding responses.

## Action Labels

```juvix
type EncryptionActionLabel :=
  | DoEncrypt EncryptRequest;
```

## Matchable Arguments

```juvix
type EncryptionMatchableArgument :=
  | ArgEncrypt EncryptRequest;
```

## Precomputation Results

```juvix
syntax alias EncryptionPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
EncryptionGuard : Type :=
  Guard
    EncryptionLocalState
    EncryptionMsg
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionMatchableArgument
    EncryptionActionLabel
    EncryptionPrecomputation;
```

### `encryptGuard`

```juvix
encryptGuard
  (t : TimestampedTrigger EncryptionMsg EncryptionTimerHandle)
  (env : EncryptionEnvironment)
  : Maybe (GuardOutput EncryptionMatchableArgument EncryptionActionLabel EncryptionPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgEncryptRequest request) := just (mkGuardOutput@{
        args := [ArgEncrypt request];
        label := DoEncrypt request;
        other := unit
      })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and produces the encryption response.

```juvix
EncryptionActionInput : Type :=
  ActionInput
    EncryptionLocalState
    EncryptionMsg
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionMatchableArgument
    EncryptionActionLabel
    EncryptionPrecomputation;

EncryptionActionEffect : Type :=
  ActionEffect
    EncryptionLocalState
    EncryptionMsg
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionMatchableArgument
    EncryptionActionLabel
    EncryptionPrecomputation;
```

### `encryptionAction`

```juvix
-- Not yet implemented
axiom encryptData : ExternalIdentity -> ByteString -> Either String ByteString;
axiom resolveReadsFor : ExternalIdentity -> ExternalIdentity;

encryptionAction
  (input : EncryptionActionInput)
  : EncryptionActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
  in
  case GuardOutput.label out of {
    | DoEncrypt request := let
        finalIdentity := case EncryptRequest.useReadsFor request of {
                           | true := (resolveReadsFor (EncryptRequest.externalIdentity request))
                           | false := (EncryptRequest.externalIdentity request)
                           };
        encryptedData := encryptData finalIdentity (EncryptRequest.data request);
        responseMsgEnc := case encryptedData of {
          | Left errorMsg := MsgEncryptResponse (mkEncryptResponse@{
              ciphertext := emptyByteString; -- Placeholder
              error := just errorMsg
            })
          | Right ciphertext' := MsgEncryptResponse (mkEncryptResponse@{
              ciphertext := ciphertext';
              error := nothing
            })
        };
        senderEnc := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetEnc := case senderEnc of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetEnc;
            mailbox := nothing;
            message := Anoma.MsgEncryption responseMsgEnc
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
encryptionConflictSolver : Set EncryptionMatchableArgument -> List (Set EncryptionMatchableArgument)
  | _ := [];
```


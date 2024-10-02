---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- decryption
- engine-dynamics
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.decryption_dynamics;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.decryption_environment open;
    import node_architecture.engines.decryption_overview open;
    import node_architecture.types.identity_types open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# Decryption Engine Dynamics

## Overview

The dynamics of the Decryption Engine define how it processes incoming decryption requests and produces the corresponding responses.

## Action Labels

```juvix
type DecryptionActionLabel :=
  | DoDecrypt DecryptRequest;
```

## Matchable Arguments

```juvix
type DecryptionMatchableArgument :=
  | ArgDecrypt DecryptRequest;
```

## Precomputation Results

```juvix
syntax alias DecryptionPrecomputation := Unit;
```

## Guards

We define guards that determine when actions are triggered based on incoming messages.

```juvix
DecryptionGuard : Type :=
  Guard
    DecryptionLocalState
    DecryptionMsg
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionMatchableArgument
    DecryptionActionLabel
    DecryptionPrecomputation;
```

### `decryptGuard`

```juvix
decryptGuard
  (t : TimestampedTrigger DecryptionMsg DecryptionTimerHandle)
  (env : DecryptionEnvironment)
  : Maybe (GuardOutput DecryptionMatchableArgument DecryptionActionLabel DecryptionPrecomputation)
  :=
  case getMessageFromTimestampedTrigger t of {
    | just (MsgDecryptRequest request) := just (mkGuardOutput@{
        args := [ArgDecrypt request];
        label := DoDecrypt request;
        other := unit
      })
    | _ := nothing
  };
```

## Action Function

We define the action function that processes the action labels and updates the environment accordingly.

```juvix
DecryptionActionInput : Type :=
  ActionInput
    DecryptionLocalState
    DecryptionMsg
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionMatchableArgument
    DecryptionActionLabel
    DecryptionPrecomputation;

DecryptionActionEffect : Type :=
  ActionEffect
    DecryptionLocalState
    DecryptionMsg
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionMatchableArgument
    DecryptionActionLabel
    DecryptionPrecomputation;
```

#### `decryptionAction`

```juvix
-- Not yet implemented
axiom decryptData : DecryptionKey -> ByteString -> Either String ByteString;

decryptionAction
  (input : DecryptionActionInput)
  : DecryptionActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoDecrypt request := let
        decryptedData := decryptData (DecryptionLocalState.decryptionKey localState) (DecryptRequest.data request);
        responseMsgDec := case decryptedData of {
          | Left errorMsg := MsgDecryptResponse (mkDecryptResponse@{
              data := emptyByteString;
              error := just errorMsg
            })
          | Right plaintext := MsgDecryptResponse (mkDecryptResponse@{
              data := plaintext;
              error := nothing
            })
        };
        senderDec := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetDec := case senderDec of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetDec;
            mailbox := nothing;
            message := Anoma.MsgDecryption responseMsgDec
          }
        }];
        timers := [];
        spawnedEngines := []
      }
  };
```

## Conflict Solver

```juvix
decryptionConflictSolver : Set DecryptionMatchableArgument -> List (Set DecryptionMatchableArgument)
  | _ := [];
```

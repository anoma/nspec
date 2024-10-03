---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- decryption
- engine-dynamics
---

??? note "Juvix preamble"

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

# `Decryption` Dynamics

## Overview

The dynamics of the Decryption Engine define how it processes incoming decryption requests and produces the corresponding responses.

## Action labels

<!-- --8<-- [start:decryption-action-label] -->
```juvix
type DecryptionActionLabel :=
  | -- --8<-- [start:DoDecrypt]
    DoDecrypt DecryptionMsg
    -- --8<-- [end:DoDecrypt]
;
```
<!-- --8<-- [end:decryption-action-label] -->

### `DoDecrypt`

!!! quote ""

    --8<-- "./decryption_dynamics.juvix.md:DoDecrypt"

This action label corresponds to decrypting the data in the given request.

??? quote "`DoDecrypt` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged. |
    | Messages to be sent   | A `DecryptResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:decryption-matchable-argument] -->
```juvix
type DecryptionMatchableArgument :=
  | -- --8<-- [start:ArgDecrypt]
    ArgDecrypt DecryptionMsg
    -- --8<-- [end:ArgDecrypt]
;
```
<!-- --8<-- [end:decryption-matchable-argument] -->

### `ArgDecrypt`

!!! quote ""

    ```
    --8<-- "./decryption_dynamics.juvix.md:ArgDecrypt"
    ```

This matchable argument contains the decryption request data.

## Precomputation results

The Decryption Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:decryption-precomputation-entry] -->
```juvix
syntax alias DecryptionPrecomputation := Unit;
```
<!-- --8<-- [end:decryption-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

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

<figure markdown>
```mermaid
flowchart TD
    C{DecryptRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoDecrypt])
```
<figcaption>decryptGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:decrypt-guard] -->
```juvix
decryptGuard
  (t : TimestampedTrigger DecryptionMsg DecryptionTimerHandle)
  (env : DecryptionEnvironment) : Maybe (GuardOutput DecryptionMatchableArgument DecryptionActionLabel DecryptionPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (DecryptRequest data) := just (
        mkGuardOutput@{
          args := [ArgDecrypt (DecryptRequest data)];
          label := DoDecrypt (DecryptRequest data);
          other := unit
        })
      | _ := nothing
  };
```
<!-- --8<-- [end:decrypt-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

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

<!-- --8<-- [start:action-function] -->
```juvix
-- Not yet implemented
axiom decryptData : DecryptionKey -> ByteString -> Either String ByteString;

axiom dummyActionEffect : DecryptionActionEffect;

decryptionAction (input : DecryptionActionInput) : DecryptionActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoDecrypt (DecryptRequest data) := let
        decryptedData := decryptData (DecryptionLocalState.decryptionKey localState) data;
        responseMsgDec := case decryptedData of {
          | Left errorMsg := DecryptResponse@{
              data := emptyByteString;
              error := just errorMsg
            }
          | Right plaintext := DecryptResponse@{
              data := plaintext;
              error := nothing
            }
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
    | DoDecrypt (DecryptResponse _ _) := dummyActionEffect
  };
```
<!-- --8<-- [end:action-function] -->

## Conflict solver

```juvix
decryptionConflictSolver : Set DecryptionMatchableArgument -> List (Set DecryptionMatchableArgument)
  | _ := [];
```

## `Decryption` Engine Summary

--8<-- "./docs/node_architecture/engines/decryption.juvix.md:decryption-engine-family"

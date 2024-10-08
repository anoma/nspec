---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- encryption
- engine-dynamics
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.encryption_dynamics;

    import prelude open;
    import node_architecture.basics open;
    import system_architecture.identity.identity open hiding {ExternalIdentity};
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.encryption_environment open;
    import node_architecture.engines.encryption_overview open;
    import node_architecture.identity_types open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# `Encryption` Dynamics

## Overview

The dynamics of the Encryption Engine define how it processes incoming encryption requests and produces the corresponding responses.

## Action labels

<!-- --8<-- [start:encryption-action-label] -->
```juvix
type EncryptionActionLabel :=
  | -- --8<-- [start:DoEncrypt]
    DoEncrypt {
      data : ByteString;
      externalIdentity : ExternalIdentity;
      useReadsFor : Bool
    }
    -- --8<-- [end:DoEncrypt]
;
```
<!-- --8<-- [end:encryption-action-label] -->

### `DoEncrypt`

!!! quote ""

    --8<-- "./encryption_dynamics.juvix.md:DoEncrypt"

This action label corresponds to encrypting the data in the given request.

??? quote "`DoEncrypt` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged (stateless operation). |
    | Messages to be sent   | An `EncryptResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:encryption-matchable-argument] -->

```juvix
type EncryptionMatchableArgument :=
  | -- --8<-- [start:ReplyTo]
  ReplyTo (Maybe Address) (Maybe MailboxID)
  -- --8<-- [end:ReplyTo]
;
```
<!-- --8<-- [end:encryption-matchable-argument] -->

### `ReplyTo`

!!! quote ""

    ```
    --8<-- "./docs/node_architecture/engines/encryption_dynamics.juvix.md:ReplyTo"
    ```

This matchable argument contains the address and mailbox ID of where the response message should be sent.

## Precomputation results

The Encryption Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:encryption-precomputation-entry] -->
```juvix
syntax alias EncryptionPrecomputation := Unit;
```
<!-- --8<-- [end:encryption-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

    ```juvix
    -- --8<-- [start:encryption-guard]
    EncryptionGuard : Type :=
      Guard
        EncryptionLocalState
        EncryptionMsg
        EncryptionMailboxState
        EncryptionTimerHandle
        EncryptionMatchableArgument
        EncryptionActionLabel
        EncryptionPrecomputation;
    -- --8<-- [end:encryption-guard]

    -- --8<-- [start:encryption-guard-output]
    EncryptionGuardOutput : Type :=
      GuardOutput EncryptionMatchableArgument EncryptionActionLabel EncryptionPrecomputation;
    -- --8<-- [end:encryption-guard-output]
    ```

### `encryptGuard`

<figure markdown>
```mermaid
flowchart TD
    C{EncryptRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoEncrypt])
```
<figcaption>encryptGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:encrypt-guard] -->
```juvix
encryptGuard
  (t : TimestampedTrigger EncryptionMsg EncryptionTimerHandle)
  (env : EncryptionEnvironment) : Maybe EncryptionGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (EncryptRequest data externalIdentity useReadsFor) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [ReplyTo (just sender) nothing] ;
                  label := DoEncrypt data externalIdentity useReadsFor;
                  other := unit
                });
        }
      | _ := nothing
  };
```
<!-- --8<-- [end:encrypt-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

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

<!-- --8<-- [start:action-function] -->
```juvix
-- Not yet implemented
axiom resolveReadsFor : ExternalIdentity -> ExternalIdentity;

encryptionAction (input : EncryptionActionInput) : EncryptionActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoEncrypt data externalIdentity useReadsFor := 
      case GuardOutput.args out of {
        | (ReplyTo (just whoAsked) _) :: _ := let
            finalIdentity := case useReadsFor of {
              | true := resolveReadsFor externalIdentity
              | false := externalIdentity
            };
            encryptedData := 
              Encryptor.encrypt (EncryptionLocalState.encryptor localState)
                (EncryptionLocalState.backend localState)
                data;
            responseMsg := EncryptResponse@{
                  ciphertext := encryptedData;
                  error := nothing
                };
          in mkActionEffect@{
            newEnv := env; -- No state change
            producedMessages := [mkEnvelopedMessage@{
              sender := just (EngineEnvironment.name env);
              packet := mkMessagePacket@{
                target := whoAsked;
                mailbox := just 0;
                message := Anoma.MsgEncryption responseMsg
              }
            }];
            timers := [];
            spawnedEngines := []
          }
        | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }
  };
```
<!-- --8<-- [end:action-function] -->

## Conflict solver

```juvix
encryptionConflictSolver : Set EncryptionMatchableArgument -> List (Set EncryptionMatchableArgument)
  | _ := [];
```

## `Encryption` Engine Summary

--8<-- "./docs/node_architecture/engines/encryption.juvix.md:encryption-engine-family"

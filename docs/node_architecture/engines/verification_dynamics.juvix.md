---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- verification
- engine-dynamics
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.verification_dynamics;

    import prelude open;
    import node_architecture.basics open;
    import Stdlib.Trait.Ord as Ord;
    import Stdlib.Data.List.Base open;
    import system_architecture.identity.identity open hiding {ExternalIdentity};
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.verification_environment open;
    import node_architecture.engines.verification_overview open;
    import node_architecture.engines.signs_for_overview open;
    import node_architecture.identity_types open;
    import node_architecture.types.anoma_message open;
    ```

# `Verification` Dynamics

## Overview

The dynamics of the Verification Engine define how it processes incoming verification requests and produces the corresponding responses.

## Action labels

<!-- --8<-- [start:verification-action-label] -->
```juvix
type VerificationActionLabel :=
  | -- --8<-- [start:DoVerify]
    DoVerify {
      data : Signable;
      commitment : Commitment;
      externalIdentity : ExternalIdentity;
      useSignsFor : Bool
    }
    -- --8<-- [end:DoVerify]
  | -- --8<-- [start:DoHandleSignsForResponse]
    DoHandleSignsForResponse {
      externalIdentity : ExternalIdentity;
      signsForEvidence : Set SignsForEvidence
    };
    -- --8<-- [end:DoHandleSignsForResponse]
;
```
<!-- --8<-- [end:verification-action-label] -->

### `DoVerify`

!!! quote ""

    --8<-- "./verification_dynamics.juvix.md:DoVerify"

This action label corresponds to verifying a commitment.

??? quote "`DoVerify` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | If `useSignsFor` is true, the state is updated to store pending requests. Otherwise, the state remains unchanged. |
    | Messages to be sent   | If `useSignsFor` is false, a `VerifyResponse` message is sent back to the requester. If `useSignsFor` is true and it's the first request for this identity, a `QuerySignsForEvidenceRequest` is sent to the SignsFor Engine. |
    | Engines to be spawned | No engines are created by this action. |
    | Timer updates         | No timers are set or cancelled. |

### `DoHandleSignsForResponse`

!!! quote ""

    --8<-- "./verification_dynamics.juvix.md:DoHandleSignsForResponse"

This action label corresponds to receiving signs for evidence and using it to address relevant pending requests.

??? quote "`DoHandleSignsForResponse` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state is updated to remove the processed pending requests for the given external identity. |
    | Messages to be sent   | `VerifyResponse` messages are sent to all requesters who were waiting for this SignsFor evidence. |
    | Engines to be spawned | No engines are created by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:verification-matchable-argument] -->

```juvix
type VerificationMatchableArgument :=
  | -- --8<-- [start:ReplyTo]
  ReplyTo (Maybe Address) (Maybe MailboxID)
  -- --8<-- [end:ReplyTo]
;
```
<!-- --8<-- [end:verification-matchable-argument] -->

### `ReplyTo`

!!! quote ""

    ```
    --8<-- "./docs/node_architecture/engines/verification_dynamics.juvix.md:ReplyTo"
    ```

This matchable argument contains the address and mailbox ID of where the response message should be sent.

## Precomputation results

The Verification Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:verification-precomputation-entry] -->
```juvix
syntax alias VerificationPrecomputation := Unit;
```
<!-- --8<-- [end:verification-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

    ```juvix
    -- --8<-- [start:verification-guard]
    VerificationGuard : Type :=
      Guard
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationMatchableArgument
        VerificationActionLabel
        VerificationPrecomputation;
    -- --8<-- [end:verification-guard]

    -- --8<-- [start:verification-guard-output]
    VerificationGuardOutput : Type :=
      GuardOutput VerificationMatchableArgument VerificationActionLabel VerificationPrecomputation;
    -- --8<-- [end:verification-guard-output]
    ```

### `verifyGuard`

<figure markdown>
```mermaid
flowchart TD
    C{VerifyRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoVerify])
```
<figcaption>verifyGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:verify-guard] -->
```juvix
verifyGuard
  (t : TimestampedTrigger VerificationTimerHandle)
  (env : VerificationEnvironment) : Maybe VerificationGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (MsgVerification (VerifyRequest x y z w)) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [ReplyTo (just sender) nothing] ;
                  label := DoVerify x y z w;
                  other := unit
                });
        }
      | _ := nothing
  };
```
<!-- --8<-- [end:verify-guard] -->

### `signsForResponseGuard`

<!-- --8<-- [start:signs-for-response-guard] -->
```juvix
signsForResponseGuard
  (t : TimestampedTrigger VerificationTimerHandle)
  (env : VerificationEnvironment) : Maybe VerificationGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (MsgSignsFor (QuerySignsForEvidenceResponse externalIdentity evidence error)) :=
          case getMessageSenderFromTimestampedTrigger t of {
            | just sender :=
                case Ord.isEQ (Ord.cmp sender (VerificationLocalState.signsForEngineAddress (EngineEnvironment.localState env))) of {
                  | true := just (mkGuardOutput@{
                      args := [];
                      label := DoHandleSignsForResponse externalIdentity evidence;
                      other := unit
                    })
                  | false := nothing
                }
            | nothing := nothing
          }
      | _ := nothing
  };
```
<!-- --8<-- [end:signs-for-response-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

    ```juvix
    VerificationActionInput : Type :=
      ActionInput
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationMatchableArgument
        VerificationActionLabel
        VerificationPrecomputation;

    VerificationActionEffect : Type :=
      ActionEffect
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationMatchableArgument
        VerificationActionLabel
        VerificationPrecomputation;
    ```

<!-- --8<-- [start:action-function] -->
```juvix
verifyResponse (externalIdentity : ExternalIdentity) (env : VerificationEnvironment) (evidence : Set SignsForEvidence) (req : Pair Address (Pair Signable Commitment)) : EnvelopedMessage :=
  let localState := EngineEnvironment.localState env;
      whoAsked := fst req;
      input := snd req;
      data := fst input;
      commitment := snd input;
      result' :=
        Verifier.verify
          (VerificationLocalState.verifier localState evidence externalIdentity)
          (VerificationLocalState.backend localState)
          data commitment;
      responseMsg := VerifyResponse@{
        result := result';
        error := nothing
      };
      envelope := mkEnvelopedMessage@{
        sender := just (EngineEnvironment.name env);
        packet := mkMessagePacket@{
          target := whoAsked;
          mailbox := just 0;
          message := MsgVerification responseMsg
        }
      };
      in envelope;

verificationAction (input : VerificationActionInput) : VerificationActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoVerify data commitment externalIdentity' useSignsFor := 
        case GuardOutput.args out of {
          | (ReplyTo (just whoAsked) _) :: _ :=
              case useSignsFor of {
                | false := 
                    let result' := 
                      Verifier.verify
                        (VerificationLocalState.verifier localState
                          Set.empty
                          externalIdentity')
                        (VerificationLocalState.backend localState)
                        data commitment;
                        responseMsg := VerifyResponse@{
                          result := result';
                          error := nothing
                        };
                        envelope := mkEnvelopedMessage@{
                          sender := just (EngineEnvironment.name env);
                          packet := mkMessagePacket@{
                            target := whoAsked;
                            mailbox := just 0;
                            message := MsgVerification responseMsg
                          }
                        };
                    in mkActionEffect@{
                      newEnv := env; -- No state change
                      producedMessages := [envelope];
                      timers := [];
                      spawnedEngines := []
                    }
                | true := 
                    -- Need to request SignsForEvidence from SignsFor Engine
                    let existingRequests := Map.lookup externalIdentity' (VerificationLocalState.pendingRequests localState);
                        newPendingList := case existingRequests of {
                          | just reqs := reqs ++ [mkPair whoAsked (mkPair commitment data)]
                          | nothing := [mkPair whoAsked (mkPair commitment data)]
                        };
                        newPendingRequests := Map.insert externalIdentity' newPendingList (VerificationLocalState.pendingRequests localState);
                        newLocalState := localState@VerificationLocalState{
                          pendingRequests := newPendingRequests
                        };
                        newEnv' := env@EngineEnvironment{
                          localState := newLocalState
                        };
                        -- Only send request to SignsFor Engine if this is the first pending request for this identity
                        messagesToSend := case existingRequests of {
                          | just _ := [] -- Request already sent, do nothing
                          | nothing := let requestMsg := QuerySignsForEvidenceRequest@{
                                          externalIdentity := externalIdentity'
                                        };
                                        envelope := mkEnvelopedMessage@{
                                          sender := just (EngineEnvironment.name env);
                                          packet := mkMessagePacket@{
                                            target := VerificationLocalState.signsForEngineAddress localState;
                                            mailbox := just 0;
                                            message := MsgSignsFor requestMsg
                                          }
                                        };
                                        in [envelope]
                        };
                    in mkActionEffect@{
                      newEnv := newEnv';
                      producedMessages := messagesToSend;
                      timers := [];
                      spawnedEngines := []
                    }
              }
          | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }
    | DoHandleSignsForResponse externalIdentity evidence := 
        -- Retrieve pending requests
        case Map.lookup externalIdentity (VerificationLocalState.pendingRequests localState) of {
          | just reqs := 
              let messages := map (verifyResponse externalIdentity env evidence) reqs;
                  newPendingRequests := Map.delete externalIdentity (VerificationLocalState.pendingRequests localState);
                  newLocalState := localState@VerificationLocalState{
                    pendingRequests := newPendingRequests
                  };
                  newEnv' := env@EngineEnvironment{
                    localState := newLocalState
                  };
              in mkActionEffect@{
                newEnv := newEnv';
                producedMessages := messages;
                timers := [];
                spawnedEngines := []
              }
          | nothing := 
              -- No pending requests, do nothing
              mkActionEffect@{
                newEnv := env;
                producedMessages := [];
                timers := [];
                spawnedEngines := []
              }
        }
  };
```
<!-- --8<-- [end:action-function] -->

## Conflict solver

```juvix
verificationConflictSolver : Set VerificationMatchableArgument -> List (Set VerificationMatchableArgument)
  | _ := [];
```

## `Verification` Engine Summary

--8<-- "./docs/node_architecture/engines/verification.juvix.md:verification-engine-family"

---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- commitment
- engine-dynamics
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.commitment_dynamics;

    import prelude open;
    import node_architecture.basics open;
    import system_architecture.identity.identity open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.identity_types open;
    import node_architecture.engines.commitment_overview open;
    import node_architecture.engines.commitment_environment open;
    import node_architecture.types.anoma_message open;
    ```

# `Commitment` Dynamics

## Overview

The dynamics of the Commitment Engine define how it processes incoming commitment requests and produces the corresponding responses.

## Action labels

<!-- --8<-- [start:commitment-action-label] -->
```juvix
type CommitmentActionLabel :=
  | -- --8<-- [start:DoCommit]
    DoCommit {
      data : Signable
    }
    -- --8<-- [end:DoCommit]
;
```
<!-- --8<-- [end:commitment-action-label] -->

### `DoCommit`

!!! quote ""

    --8<-- "./commitment_dynamics.juvix.md:DoCommit"

This action label corresponds to generating a commitment (signature) for the given request.

??? quote "`DoCommit` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged. |
    | Messages to be sent   | A `CommitResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:commitment-matchable-argument] -->

```juvix
type CommitmentMatchableArgument :=
  | -- --8<-- [start:ReplyTo]
  ReplyTo (Maybe Address) (Maybe MailboxID)
  -- --8<-- [end:ReplyTo]
;
```
<!-- --8<-- [end:commitment-matchable-argument] -->

### `ReplyTo`

!!! quote ""

    ```
    --8<-- "./docs/node_architecture/engines/commitment_dynamics.juvix.md:ReplyTo"
    ```

This matchable argument contains the address and mailbox ID of where the response message should be sent.

## Precomputation results

The Commitment Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:commitment-precomputation-entry] -->
```juvix
syntax alias CommitmentPrecomputation := Unit;
```
<!-- --8<-- [end:commitment-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

    ```juvix
    -- --8<-- [start:commitment-guard]
    CommitmentGuard : Type :=
      Guard
        CommitmentLocalState
        CommitmentMailboxState
        CommitmentTimerHandle
        CommitmentMatchableArgument
        CommitmentActionLabel
        CommitmentPrecomputation;
    -- --8<-- [end:commitment-guard]

    -- --8<-- [start:commitment-guard-output]
    CommitmentGuardOutput : Type :=
      GuardOutput CommitmentMatchableArgument CommitmentActionLabel CommitmentPrecomputation;
    -- --8<-- [end:commitment-guard-output]
    ```

### `commitGuard`

<figure markdown>
```mermaid
flowchart TD
    C{CommitRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoCommit])
```
<figcaption>commitGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:commit-guard] -->
```juvix
commitGuard
  (t : TimestampedTrigger CommitmentTimerHandle)
  (env : CommitmentEnvironment) : Maybe CommitmentGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (MsgCommitment (CommitRequest data)) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [ReplyTo (just sender) nothing] ;
                  label := DoCommit data;
                  other := unit
                });
        }
      | _ := nothing
  };
```
<!-- --8<-- [end:commit-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

    ```juvix
    CommitmentActionInput : Type :=
      ActionInput
        CommitmentLocalState
        CommitmentMailboxState
        CommitmentTimerHandle
        CommitmentMatchableArgument
        CommitmentActionLabel
        CommitmentPrecomputation;

    CommitmentActionEffect : Type :=
      ActionEffect
        CommitmentLocalState
        CommitmentMailboxState
        CommitmentTimerHandle
        CommitmentMatchableArgument
        CommitmentActionLabel
        CommitmentPrecomputation;
    ```

<!-- --8<-- [start:action-function] -->
```juvix
commitmentAction (input : CommitmentActionInput) : CommitmentActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoCommit data := 
      case GuardOutput.args out of {
        | (ReplyTo (just whoAsked) _) :: _ := let
            signedData := 
              Signer.sign (CommitmentLocalState.signer localState) 
                (CommitmentLocalState.backend localState)
                data;
            responseMsg := CommitResponse@{
                  commitment := signedData
                };
          in mkActionEffect@{
            newEnv := env; -- No state change
            producedMessages := [mkEnvelopedMessage@{
              sender := just (EngineEnvironment.name env);
              packet := mkMessagePacket@{
                target := whoAsked;
                mailbox := just 0;
                message := MsgCommitment responseMsg
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
commitmentConflictSolver : Set CommitmentMatchableArgument -> List (Set CommitmentMatchableArgument)
  | _ := [];
```

## `Commitment` Engine Summary

--8<-- "./docs/node_architecture/engines/commitment.juvix.md:commitment-engine-family"
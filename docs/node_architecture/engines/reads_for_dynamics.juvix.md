---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- reads_for
- engine-dynamics
---

??? note "Juvix preamble"

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

# `Reads For` Dynamics

## Overview

The dynamics of the Reads For Engine define how it processes incoming messages and updates its state accordingly.

## Action labels

<!-- --8<-- [start:reads-for-action-label] -->
```juvix
type ReadsForActionLabel :=
  | -- --8<-- [start:DoReadsForQuery]
    DoReadsForQuery {
      externalIdentityA : ExternalIdentity;
      externalIdentityB : ExternalIdentity
    }
    -- --8<-- [end:DoReadsForQuery]
  | -- --8<-- [start:DoSubmitEvidence]
    DoSubmitEvidence {
      evidence : ReadsForEvidence
    }
    -- --8<-- [end:DoSubmitEvidence]
  | -- --8<-- [start:DoQueryEvidence]
    DoQueryEvidence {
      externalIdentity : ExternalIdentity
    }
    -- --8<-- [end:DoQueryEvidence]
;
```
<!-- --8<-- [end:reads-for-action-label] -->

### `DoReadsForQuery`

!!! quote ""

    --8<-- "./reads_for_dynamics.juvix.md:DoReadsForQuery"

This action label corresponds to processing a reads_for query.

??? quote "`DoReadsForQuery` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged. |
    | Messages to be sent   | A `ReadsForResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

### `DoSubmitEvidence`

!!! quote ""

    --8<-- "./reads_for_dynamics.juvix.md:DoSubmitEvidence"

This action label corresponds to submitting new reads_for evidence.

??? quote "`DoSubmitEvidence` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The new evidence is added to the evidence store. |
    | Messages to be sent   | A `SubmitReadsForEvidenceResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

### `DoQueryEvidence`

!!! quote ""

    --8<-- "./reads_for_dynamics.juvix.md:DoQueryEvidence"

This action label corresponds to querying reads_for evidence for a specific identity.

??? quote "`DoQueryEvidence` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged. |
    | Messages to be sent   | A `QueryReadsForEvidenceResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:reads-for-matchable-argument] -->

```juvix
type ReadsForMatchableArgument :=
  | -- --8<-- [start:ReplyTo]
  ReplyTo (Maybe Address) (Maybe MailboxID)
  -- --8<-- [end:ReplyTo]
;
```
<!-- --8<-- [end:reads-for-matchable-argument] -->

### `ReplyTo`

!!! quote ""

    ```
    --8<-- "./docs/node_architecture/engines/reads_for_dynamics.juvix.md:ReplyTo"
    ```

This matchable argument contains the address and mailbox ID of where the response message should be sent.

## Precomputation results

The Reads For Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:reads-for-precomputation-entry] -->
```juvix
syntax alias ReadsForPrecomputation := Unit;
```
<!-- --8<-- [end:reads-for-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

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

<figure markdown>
```mermaid
flowchart TD
    C{ReadsForRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoReadsForQuery])
```
<figcaption>readsForQueryGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:reads-for-query-guard] -->
```juvix
readsForQueryGuard
  (t : TimestampedTrigger ReadsForMsg ReadsForTimerHandle)
  (env : ReadsForEnvironment) : Maybe (GuardOutput ReadsForMatchableArgument ReadsForActionLabel ReadsForPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (ReadsForRequest x y) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [ReplyTo (just sender) nothing] ;
          label := DoReadsForQuery x y;
          other := unit
        });}
      | _ := nothing
  };
```
<!-- --8<-- [end:reads-for-query-guard] -->

### `submitEvidenceGuard`

<figure markdown>
```mermaid
flowchart TD
    C{SubmitReadsForEvidence<br>Request received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoSubmitEvidence])
```
<figcaption>submitEvidenceGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:submit-evidence-guard] -->
```juvix
submitEvidenceGuard
  (t : TimestampedTrigger ReadsForMsg ReadsForTimerHandle)
  (env : ReadsForEnvironment) : Maybe (GuardOutput ReadsForMatchableArgument ReadsForActionLabel ReadsForPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (SubmitReadsForEvidenceRequest x) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [ReplyTo (just sender) nothing] ;
          label := DoSubmitEvidence x;
          other := unit
        });}
      | _ := nothing
  };
```
<!-- --8<-- [end:submit-evidence-guard] -->

### `queryEvidenceGuard`

<figure markdown>
```mermaid
flowchart TD
    C{QueryReadsForEvidence<br>Request received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoQueryEvidence])
```
<figcaption>queryEvidenceGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:query-evidence-guard] -->
```juvix
queryEvidenceGuard
  (t : TimestampedTrigger ReadsForMsg ReadsForTimerHandle)
  (env : ReadsForEnvironment) : Maybe (GuardOutput ReadsForMatchableArgument ReadsForActionLabel ReadsForPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (QueryReadsForEvidenceRequest x) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [ReplyTo (just sender) nothing] ;
                  label := DoQueryEvidence x;
                  other := unit
                });
        }
      | _ := nothing
  };
```
<!-- --8<-- [end:query-evidence-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

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

<!-- --8<-- [start:action-function] -->
```juvix
readsForAction (input : ReadsForActionInput) : ReadsForActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoReadsForQuery externalIdentityA externalIdentityB :=
      case GuardOutput.args out of {
        | (ReplyTo (just whoAsked) _) :: _ := let
            hasEvidence := elem \{a b := a && b} true (map \{ evidence :=
              isEQ (Ord.cmp (ReadsForEvidence.fromIdentity evidence) externalIdentityA) &&
              isEQ (Ord.cmp (ReadsForEvidence.toIdentity evidence) externalIdentityB)
            } (toList (ReadsForLocalState.evidenceStore localState)));
            responseMsg := ReadsForResponse@{
              readsFor := hasEvidence;
              error := nothing
            };
          in mkActionEffect@{
            newEnv := env; -- No state change
            producedMessages := [mkEnvelopedMessage@{
              sender := just (EngineEnvironment.name env);
              packet := mkMessagePacket@{
                target := whoAsked;
                mailbox := just 0;
                message := Anoma.MsgReadsFor responseMsg
              }
            }];
            timers := [];
            spawnedEngines := []
          }
        | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }
    | DoSubmitEvidence evidence :=
      case GuardOutput.args out of {
        | (ReplyTo (just whoAsked) _) :: _ := let
            newEvidenceStore := Set.insert evidence (ReadsForLocalState.evidenceStore localState);
            newLocalState := mkReadsForLocalState@{
              evidenceStore := newEvidenceStore
            };
            newEnv' := env@EngineEnvironment{
              localState := newLocalState
            };
            responseMsg := SubmitReadsForEvidenceResponse@{
              error := nothing
            };
          in mkActionEffect@{
            newEnv := newEnv';
            producedMessages := [mkEnvelopedMessage@{
              sender := just (EngineEnvironment.name env);
              packet := mkMessagePacket@{
                target := whoAsked;
                mailbox := just 0;
                message := Anoma.MsgReadsFor responseMsg
              }
            }];
            timers := [];
            spawnedEngines := []
          }
        | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }
    | DoQueryEvidence externalIdentity :=
      case GuardOutput.args out of {
        | (ReplyTo (just whoAsked) _) :: _ := let
            relevantEvidence := AVLfilter \{evidence :=
              isEQ (Ord.cmp (ReadsForEvidence.fromIdentity evidence) externalIdentity) ||
              isEQ (Ord.cmp (ReadsForEvidence.toIdentity evidence) externalIdentity)
            } (ReadsForLocalState.evidenceStore localState);
            responseMsg := QueryReadsForEvidenceResponse@{
              evidence := relevantEvidence;
              error := nothing
            };
          in mkActionEffect@{
            newEnv := env; -- No state change
            producedMessages := [mkEnvelopedMessage@{
              sender := just (EngineEnvironment.name env);
              packet := mkMessagePacket@{
                target := whoAsked;
                mailbox := just 0;
                message := Anoma.MsgReadsFor responseMsg
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
readsForConflictSolver : Set ReadsForMatchableArgument -> List (Set ReadsForMatchableArgument)
  | _ := [];
```

## `Reads For` Engine Summary

--8<-- "./docs/node_architecture/engines/reads_for.juvix.md:reads-for-engine-family"

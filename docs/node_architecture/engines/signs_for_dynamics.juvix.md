---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- signs_for
- engine-dynamics
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.signs_for_dynamics;

    import prelude open;
    import Stdlib.Data.List.Base open;
    import Data.Set.AVL open;
    import Stdlib.Trait.Ord open;
    import Stdlib.Data.Bool.Base open;
    import node_architecture.basics open;
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.identity_types open;
    import node_architecture.engines.signs_for_environment open;
    import node_architecture.engines.signs_for_overview open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# `Signs For` Dynamics

## Overview

The dynamics of the Signs For Engine define how it processes incoming messages and updates its state accordingly.

## Action labels

<!-- --8<-- [start:signs-for-action-label] -->
```juvix
type SignsForActionLabel :=
  | -- --8<-- [start:DoSignsForQuery]
    DoSignsForQuery SignsForMsg
    -- --8<-- [end:DoSignsForQuery]
  | -- --8<-- [start:DoSubmitEvidence]
    DoSubmitEvidence SignsForMsg
    -- --8<-- [end:DoSubmitEvidence]
  | -- --8<-- [start:DoQueryEvidence]
    DoQueryEvidence SignsForMsg
    -- --8<-- [end:DoQueryEvidence]
;
```
<!-- --8<-- [end:signs-for-action-label] -->

### `DoSignsForQuery`

!!! quote ""

    --8<-- "./signs_for_dynamics.juvix.md:DoSignsForQuery"

This action label corresponds to processing a signs_for query.

??? quote "`DoSignsForQuery` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged. |
    | Messages to be sent   | A `SignsForResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

### `DoSubmitEvidence`

!!! quote ""

    --8<-- "./signs_for_dynamics.juvix.md:DoSubmitEvidence"

This action label corresponds to submitting new signs_for evidence.

??? quote "`DoSubmitEvidence` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The new evidence is added to the evidence store. |
    | Messages to be sent   | A `SubmitSignsForEvidenceResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

### `DoQueryEvidence`

!!! quote ""

    --8<-- "./signs_for_dynamics.juvix.md:DoQueryEvidence"

This action label corresponds to querying signs_for evidence for a specific identity.

??? quote "`DoQueryEvidence` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state remains unchanged. |
    | Messages to be sent   | A `QuerySignsForEvidenceResponse` message is sent back to the requester. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:signs-for-matchable-argument] -->
```juvix
type SignsForMatchableArgument :=
  | -- --8<-- [start:ArgSignsForQuery]
    ArgSignsForQuery SignsForMsg
    -- --8<-- [end:ArgSignsForQuery]
  | -- --8<-- [start:ArgSubmitEvidence]
    ArgSubmitEvidence SignsForMsg
    -- --8<-- [end:ArgSubmitEvidence]
  | -- --8<-- [start:ArgQueryEvidence]
    ArgQueryEvidence SignsForMsg
    -- --8<-- [end:ArgQueryEvidence]
;
```
<!-- --8<-- [end:signs-for-matchable-argument] -->

### `ArgSignsForQuery`

!!! quote ""

    ```
    --8<-- "./signs_for_dynamics.juvix.md:ArgSignsForQuery"
    ```

This matchable argument contains the signs_for query request data.

### `ArgSubmitEvidence`

!!! quote ""

    ```
    --8<-- "./signs_for_dynamics.juvix.md:ArgSubmitEvidence"
    ```

This matchable argument contains the evidence submission request data.

### `ArgQueryEvidence`

!!! quote ""

    ```
    --8<-- "./signs_for_dynamics.juvix.md:ArgQueryEvidence"
    ```

This matchable argument contains the evidence query request data.

## Precomputation results

The Signs For Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:signs-for-precomputation-entry] -->
```juvix
syntax alias SignsForPrecomputation := Unit;
```
<!-- --8<-- [end:signs-for-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

    ```juvix
    SignsForGuard : Type :=
      Guard
        SignsForLocalState
        SignsForMsg
        SignsForMailboxState
        SignsForTimerHandle
        SignsForMatchableArgument
        SignsForActionLabel
        SignsForPrecomputation;
    ```

### `signsForQueryGuard`

<figure markdown>
```mermaid
flowchart TD
    C{SignsForRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoSignsForQuery])
```
<figcaption>signsForQueryGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:signs-for-query-guard] -->
```juvix
signsForQueryGuard
  (t : TimestampedTrigger SignsForMsg SignsForTimerHandle)
  (env : SignsForEnvironment) : Maybe (GuardOutput SignsForMatchableArgument SignsForActionLabel SignsForPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (SignsForRequest x y) := just (
        mkGuardOutput@{
          args := [ArgSignsForQuery (SignsForRequest x y)];
          label := DoSignsForQuery (SignsForRequest x y);
          other := unit
        })
      | _ := nothing
  };
```
<!-- --8<-- [end:signs-for-query-guard] -->

### `submitEvidenceGuard`

<figure markdown>
```mermaid
flowchart TD
    C{SubmitSignsForEvidence<br>Request received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoSubmitEvidence])
```
<figcaption>submitEvidenceGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:submit-evidence-guard] -->
```juvix
submitEvidenceGuard
  (t : TimestampedTrigger SignsForMsg SignsForTimerHandle)
  (env : SignsForEnvironment) : Maybe (GuardOutput SignsForMatchableArgument SignsForActionLabel SignsForPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (SubmitSignsForEvidenceRequest x) := just (
        mkGuardOutput@{
          args := [ArgSubmitEvidence (SubmitSignsForEvidenceRequest x)];
          label := DoSubmitEvidence (SubmitSignsForEvidenceRequest x);
          other := unit
        })
      | _ := nothing
  };
```
<!-- --8<-- [end:submit-evidence-guard] -->

### `queryEvidenceGuard`

<figure markdown>
```mermaid
flowchart TD
    C{QuerySignsForEvidence<br>Request received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoQueryEvidence])
```
<figcaption>queryEvidenceGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:query-evidence-guard] -->
```juvix
queryEvidenceGuard
  (t : TimestampedTrigger SignsForMsg SignsForTimerHandle)
  (env : SignsForEnvironment) : Maybe (GuardOutput SignsForMatchableArgument SignsForActionLabel SignsForPrecomputation)
  := case getMessageFromTimestampedTrigger t of {
      | just (QuerySignsForEvidenceRequest x) := just (
        mkGuardOutput@{
          args := [ArgQueryEvidence (QuerySignsForEvidenceRequest x) ];
          label := DoQueryEvidence (QuerySignsForEvidenceRequest x) ;
          other := unit
        })
      | _ := nothing
  };
```
<!-- --8<-- [end:query-evidence-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

    ```juvix
    SignsForActionInput : Type :=
      ActionInput
        SignsForLocalState
        SignsForMsg
        SignsForMailboxState
        SignsForTimerHandle
        SignsForMatchableArgument
        SignsForActionLabel
        SignsForPrecomputation;

    SignsForActionEffect : Type :=
      ActionEffect
        SignsForLocalState
        SignsForMsg
        SignsForMailboxState
        SignsForTimerHandle
        SignsForMatchableArgument
        SignsForActionLabel
        SignsForPrecomputation;
    ```

<!-- --8<-- [start:action-function] -->
```juvix
axiom dummyActionEffect : SignsForActionEffect;

signsForAction (input : SignsForActionInput) : SignsForActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      localState := EngineEnvironment.localState env;
  in
  case GuardOutput.label out of {
    | DoSignsForQuery (SignsForRequest externalIdentityA externalIdentityB) := let
        hasEvidence := elem \{a b := a && b} true (map \{ evidence :=
          isEQ (Ord.cmp (SignsForEvidence.fromIdentity evidence) externalIdentityA) &&
          isEQ (Ord.cmp (SignsForEvidence.toIdentity evidence) externalIdentityB)
        } (toList (SignsForLocalState.evidenceStore localState)));
        responseMsgSF := SignsForResponse@{
          signsFor := hasEvidence;
          error := nothing
        };
        senderSF := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetSF := case senderSF of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := env; -- No state change
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetSF;
            mailbox := nothing;
            message := Anoma.MsgSignsFor responseMsgSF
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoSubmitEvidence (SubmitSignsForEvidenceRequest evidence) := let
        newEvidenceStore := Set.insert evidence (SignsForLocalState.evidenceStore localState);
        newLocalStateSF := mkSignsForLocalState@{
          evidenceStore := newEvidenceStore
        };
        newEnvSF := env@EngineEnvironment{
          localState := newLocalStateSF
        };
        responseMsgSubmit := SubmitSignsForEvidenceResponse@{
          error := nothing
        };
        senderSubmit := getMessageSenderFromTimestampedTrigger (ActionInput.timestampedTrigger input);
        targetSubmit := case senderSubmit of {
          | just s := s
          | nothing := Left "unknown"
        };
      in mkActionEffect@{
        newEnv := newEnvSF;
        producedMessages := [mkEnvelopedMessage@{
          sender := just (EngineEnvironment.name env);
          packet := mkMessagePacket@{
            target := targetSubmit;
            mailbox := nothing;
            message := Anoma.MsgSignsFor responseMsgSubmit
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | DoQueryEvidence (QuerySignsForEvidenceRequest externalIdentity) := let
        relevantEvidence := AVLfilter \{evidence :=
          isEQ (Ord.cmp (SignsForEvidence.fromIdentity evidence) externalIdentity) ||
          isEQ (Ord.cmp (SignsForEvidence.toIdentity evidence) externalIdentity)
        } (SignsForLocalState.evidenceStore localState);
        responseMsgQuery := QuerySignsForEvidenceResponse@{
          evidence := relevantEvidence;
          error := nothing
        };
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
            message := Anoma.MsgSignsFor responseMsgQuery
          }
        }];
        timers := [];
        spawnedEngines := []
      }
    | _ := dummyActionEffect
  };
```
<!-- --8<-- [end:action-function] -->

## Conflict solver

```juvix
signsForConflictSolver : Set SignsForMatchableArgument -> List (Set SignsForMatchableArgument)
  | _ := [];
```

## `Signs For` Engine Summary

--8<-- "./docs/node_architecture/engines/signs_for.juvix.md:signs-for-engine-family"

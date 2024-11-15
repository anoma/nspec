---
icon: material/animation-play
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-behaviour
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.template_behaviour;

    import arch.node.engines.template_messages open;
    import arch.node.engines.template_environment open;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.engine open;
    import arch.node.types.engine_behaviour open;
    import arch.node.types.anoma_message open;
    ```

# Template Behaviour

## Overview

A template engine acts in the ways described on this page.
The action labels correspond to the actions that can be performed by the engine.
Using the action labels, we describe the effects of the actions.

## Action labels

### `TemplateActionLabelDoNothing`

This action label corresponds to doing one thing
by the `doNothingAction`
upon reception of the `MsgTemplateJustHi` message.

### `TemplateActionLabelExampleReply`

This action label corresponds to doing something
by the `exampleReplyAction`
upon reception of the `MsgTemplateExampleRequest` message.

### `TemplateActionLabel`

<!-- --8<-- [start:TemplateActionLabel] -->
```juvix
type TemplateActionLabel :=
  | TemplateActionLabelDoNothing
  | TemplateActionLabelExampleReply
;
```
<!-- --8<-- [end:TemplateActionLabel] -->

## Action arguments

The action arguments are set by a guard
and passed to the action function as part of the `GuardOutput`.

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:Val] -->
    ```juvix
    syntax alias Val := Nat;
    ```
    <!-- --8<-- [end:Val] -->

### `TemplateActionArgumentOne FirstArgument`

<!-- --8<-- [start:FirstArgument] -->
```juvix
type FirstArgument := mkFirstArgument {
  data : Val;
};
```
<!-- --8<-- [end:FirstArgument] -->

???+ quote "Arguments"

    `data`:
    : is the value of the action argument.

### `TemplateActionArgumentTwo SecondArgument`

<!-- --8<-- [start:SecondArgument] -->
```juvix
type SecondArgument := mkSecondArgument {
  data : String;
};
```
<!-- --8<-- [end:SecondArgument] -->

???+ quote "Arguments"

    `data`:
    : is the value of the action argument.

### `TemplateActionArgument`

<!-- --8<-- [start:template-action-argument] -->
```juvix
type TemplateActionArgument :=
  | TemplateActionArgumentOne FirstArgument
  | TemplateActionArgumentTwo SecondArgument
  ;
```
<!-- --8<-- [end:template-action-argument] -->

## Precomputation tasks results

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:pseudo-example-auxiliary-code] -->
    ```juvix
    syntax alias SomeMessageType := Nat;
    ```
    <!-- --8<-- [end:pseudo-example-auxiliary-code] -->

Precomputation tasks results are the outcomes generated during the
precomputation phase. These results are used to optimize and prepare the
engine's state and environment before the main computation begins (by actions).
The results of these tasks are then utilised by the engine to ensure efficient
and accurate execution of its functions.

### `TemplatePrecomputationEntryDeleteMessage DeleteMessage`

<!-- --8<-- [start:DeleteMessage] -->
```juvix
type DeleteMessage := mkDeleteMessage {
  messageType : SomeMessageType;
  messageId : Nat;
};
```
<!-- --8<-- [end:DeleteMessage] -->

We delete the given message from the mailbox with the mailbox ID.

???+ quote "Arguments"

    `messageType`:
    : is the type of the message to delete.

    `messageId`:
    : is the ID of the message to delete.

### `TemplatePrecomputationEntryCloseMailbox CloseMailbox`

<!-- --8<-- [start:CloseMailbox] -->
```juvix
type CloseMailbox := mkCloseMailbox {
  mailboxId : Nat;
};
```
<!-- --8<-- [end:CloseMailbox] -->

We close the mailbox with the given mailbox ID.

???+ quote "Arguments"

    `mailboxId`:
    : is the ID of the mailbox to close.

### `TemplatePrecomputationEntry`

<!-- --8<-- [start:TemplatePrecomputation] -->
```juvix
type TemplatePrecomputationEntry :=
  | TemplatePrecomputationEntryDeleteMessage DeleteMessage
  | TemplatePrecomputationEntryCloseMailbox CloseMailbox
  ;
```
<!-- --8<-- [end:TemplatePrecomputation] -->

### `TemplatePrecomputationList`

<!-- --8<-- [start:TemplatePrecomputationList] -->
```juvix
TemplatePrecomputationList : Type := List TemplatePrecomputationEntry;
```
<!-- --8<-- [end:TemplatePrecomputationList] -->

The precomputation results consist of a list of `TemplatePrecomputation` terms.
Each entry can be either:

1. A `DeleteMessage` entry indicating a message should be deleted from a mailbox
2. A `CloseMailbox` entry indicating a mailbox should be closed

These entries are used by guards to specify mailbox operations that need to be
performed as part of processing a message.

## Guards

???+ quote "Auxiliary Juvix code"

    ### `TemplateGuard`

    <!-- --8<-- [start:TemplateGuard] -->
    ```juvix
    TemplateGuard : Type :=
      Guard
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArgument
        TemplateActionLabel
        TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateGuard] -->

    ### `TemplateGuardOutput`

    <!-- --8<-- [start:TemplateGuardOutput] -->
    ```juvix
    TemplateGuardOutput : Type :=
      GuardOutput
        TemplateActionArgument
        TemplateActionLabel
        TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateGuardOutput] -->

### `justHiGuard`

<!-- --8<-- [start:justHiGuard] -->
```juvix
justHiGuard
  (t : TimestampedTrigger TemplateTimerHandle )
  (env : TemplateEnvironment) : Option TemplateGuardOutput :=
  case getMessageFromTimestampedTrigger t of {
  | some (MsgTemplate MsgTemplateJustHi) := some (
    mkGuardOutput@{
      actionLabel := TemplateActionLabelDoNothing;
      actionArgs := [
        (TemplateActionArgumentTwo
          mkSecondArgument@{
            data := "Hello World!"
          })
      ];
      precomputationTasks := [
        TemplatePrecomputationEntryCloseMailbox (
          mkCloseMailbox@{
            mailboxId := 1;
          }
        );
        TemplatePrecomputationEntryDeleteMessage (
          mkDeleteMessage@{
            messageType := 1337;
            messageId := 0;
          }
        )
      ];
    })
  | _ := none
  };
```
<!-- --8<-- [end:justHiGuard] -->

### `exampleRequestGuard`

<!-- --8<-- [start:exampleRequestGuard] -->
```juvix
exampleRequestGuard
  (t : TimestampedTrigger TemplateTimerHandle)
  (env : TemplateEnvironment) : Option TemplateGuardOutput :=
  case getMessageFromTimestampedTrigger t of {
  | some (MsgTemplate (MsgTemplateExampleRequest _)) := do {
    sender <- getSenderFromTimestampedTrigger t;
    pure (mkGuardOutput@{
      actionLabel := TemplateActionLabelExampleReply;
      actionArgs := [];
      precomputationTasks := []
      });
  }
  | _ := none
  };
```
<!-- --8<-- [end:exampleRequestGuard] -->

## Action functions

??? quote "Auxiliary Juvix code"

    ### `TemplateActionInput`

    <!-- --8<-- [start:TemplateActionInput] -->
    ```juvix
    TemplateActionInput : Type :=
      ActionInput
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArgument
        TemplateActionLabel
        TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateActionInput] -->

    ### `TemplateActionEffect`

    <!-- --8<-- [start:TemplateActionEffect] -->
    ```juvix
    TemplateActionEffect : Type :=
      ActionEffect
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArgument
        TemplateActionLabel
        TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateActionEffect] -->

    ### `TemplateActionFunction`

    <!-- --8<-- [start:TemplateActionFunction] -->
    ```juvix
    TemplateActionFunction : Type :=
      ActionFunction
          TemplateLocalState
          TemplateMailboxState
          TemplateTimerHandle
          TemplateActionArgument
          TemplateActionLabel
          TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateActionFunction] -->

### `doNothingAction`

Give a short description of the action function.

State update
: The state is unchanged as the timer will have all information necessary.

Messages to be sent
: No messages are added to the send queue.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

Acquaintance updates
: None.

```juvix
doNothingAction (input : TemplateActionInput) : TemplateActionEffect :=
  let
    env := ActionInput.env input;
    out := ActionInput.guardOutput input;
    msg := getMessageFromTimestampedTrigger (ActionInput.timestampedTrigger input);
  in
    case GuardOutput.actionArgs out of {
      | TemplateActionArgumentTwo (mkSecondArgument@{
          data := data;
        }) :: _ :=
        mkActionEffect@{
          newEnv := env@EngineEnvironment{
            localState := mkTemplateLocalState@{
              taskQueue := mkCustomData@{
                word := data
              }
            }
          };
          producedMessages := [];
          timers := [];
          spawnedEngines := []
        }
      | _ := mkActionEffect@{
          newEnv := env;
          producedMessages := [];
          timers := [];
          spawnedEngines := []
        }
    }
```

### `exampleReplyAction`

Responds to the `MsgTemplateExampleRequest` message,
actioned by the `TemplateActionLabelExampleReply` label.

State update
: The state remains unchanged.

Messages to be sent
: A `MsgTemplateExampleReply` message with `argOne` from the received `MsgTemplateExampleRequest`.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

```juvix
exampleReplyAction (input : TemplateActionInput) : TemplateActionEffect :=
  let
    env := ActionInput.env input;
    out := ActionInput.guardOutput input;
    msg := getMessageFromTimestampedTrigger (ActionInput.timestampedTrigger input);
  in
    case msg of {
      | some (MsgTemplate (MsgTemplateExampleRequest req)) :=
        mkActionEffect@{
          newEnv := env;
          producedMessages := [
            mkEngineMsg@{
              sender := getTargetFromActionInput input;
              target := getSenderFromActionInput input;
              mailbox := some 0;
              msg :=
                MsgTemplate
                  (MsgTemplateExampleReply
                    (ok mkExampleReplyOk@{
                      argOne := ExampleRequest.argOne req;
                    }));              
            }
          ];
          timers := [];
          spawnedEngines := []
        }
      | _ := mkActionEffect@{
          newEnv := env;
          producedMessages := [];
          timers := [];
          spawnedEngines := []
        }
    }
```

### `templateAction`

Calls the action function corresponding to the action label set by the guard.

<!-- --8<-- [start:templateAction] -->
```juvix
templateAction (input : TemplateActionInput) : TemplateActionEffect :=
  case GuardOutput.actionLabel (ActionInput.guardOutput input) of {
  | TemplateActionLabelDoNothing := doNothingAction input
  | TemplateActionLabelExampleReply := exampleReplyAction input
  };
```
<!-- --8<-- [end:templateAction] -->

## Conflict solver

The conflict solver is responsible for resolving conflicts between multiple
guards that match simultaneously. When multiple guards match the same input, the
conflict solver determines which combinations of guards can execute together.

In this template example, the conflict solver is very simple. It always returns
an empty list, meaning no guards can execute simultaneously. This effectively
serializes guard execution, allowing only one guard to execute at a time.

<!-- TODO: ask Tobias if he agrees with this description. So far, we have not
used the conflict solver in any of our examples. -->

### `templateConflictSolver`

```juvix
templateConflictSolver :
  Set TemplateActionArgument ->
  List (Set TemplateActionArgument)
  | _ := [];
```

## The Template behaviour

### `TemplateBehaviour`

<!-- --8<-- [start:TemplateBehaviour] -->
```juvix
TemplateBehaviour : Type :=
  EngineBehaviour
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateActionArgument
    TemplateActionLabel
    TemplatePrecomputationList;
```
<!-- --8<-- [end:TemplateBehaviour] -->

#### Instantiation

<!-- --8<-- [start:templateBehaviour] -->
```juvix
templateBehaviour : TemplateBehaviour :=
  mkEngineBehaviour@{
    guards := [justHiGuard; exampleRequestGuard];
    action := templateAction;
    conflictSolver := templateConflictSolver;
  }
  ;
```
<!-- --8<-- [end:templateBehaviour] -->

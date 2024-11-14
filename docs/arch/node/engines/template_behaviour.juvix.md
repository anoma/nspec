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
    import prelude open;
    import arch.node.engines.template_messages open;
    import arch.node.engines.template_environment open;
    import arch.node.types.engine_behaviour open;
    ```

# Template Behaviour

## Overview

A template engine acts in the ways described on this page.
The action labels correspond to the actions that can be performed by the engine.
Using the action labels, we describe the effects of the actions.


## Action labels

### `TemplateActionLabelDoOneThing`

This action label corresponds to doing one thing
by the `doOneThingAction`
upon reception of the `MsgTemplateJustHi` message.

#### State update

The state is unchanged as the timer will have all information necessary.

#### Messages to be sent

No messages are added to the send queue.

#### Engines to be spawned

No engine is created by this action.

#### Timer updates

No timers are set or cancelled.

#### Acquaintance updates

None.


### `TemplateActionLabelDoSomeThing String`

This action label corresponds to doing something
by the `doSomeThingAction`
upon reception of the `MsgTemplateJustHi` message.

#### State update

The state is unchanged as the timer will have all information necessary.

#### Messages to be sent

No messages are added to the send queue.

#### Engines to be spawned

No engine is created by this action.

#### Timer updates

No timers are set or cancelled.

#### Acquaintance updates

None.


### `TemplateActionLabelDoAnotherThing String`

This action label corresponds to doing another thing
by the `doAnotherThingAction`
upon reception of the `MsgTemplateJustHi` message.

#### State update

The state is unchanged as the timer will have all information necessary.

#### Messages to be sent

No messages are added to the send queue.

#### Engines to be spawned

No engine is created by this action.

#### Timer updates

No timers are set or cancelled.

#### Acquaintance updates

None.


### `TemplateActionLabelDoAlternative`

This action label corresponds to performing
either `TemplateActionLabelDoSomeThing` or `TemplateActionLabelDoAnotherThing`.


### `TemplateActionLabelDoBoth`

This action label corresponds to performing
both `TemplateActionLabelDoSomeThing` and `TemplateActionLabelDoAnotherThing`.


### `TemplateActionLabel`

<!-- --8<-- [start:SomeActionLabel] -->
```juvix
type SomeActionLabel :=
  | TemplateActionLabelDoSomeThing String
  ;
```
<!-- --8<-- [end:SomeActionLabel] -->

<!-- --8<-- [start:AnotherActionLabel] -->
```juvix
type AnotherActionLabel :=
  | TemplateActionLabelDoAnotherThing String
  ;
```
<!-- --8<-- [end:AnotherActionLabel] -->

<!-- --8<-- [start:TemplateActionLabel] -->
```juvix
type TemplateActionLabel :=
  | TemplateActionLabelDoOneThing
  | TemplateActionLabelDoAlternative (Either SomeActionLabel AnotherActionLabel)
  | TemplateActionLabelDoBoth (Pair SomeActionLabel AnotherActionLabel)
;
```
<!-- --8<-- [end:TemplateActionLabel] -->

## Matchable arguments

The matchable arguments correspond to the arguments that can be matched on in
guards. The data matched on is passed to the action function.

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:Val] -->
    ```juvix
    syntax alias Val := Nat;
    ```
    <!-- --8<-- [end:Val] -->

### `TemplateMatchableArgumentFirstOption FirstOptionMatchableArgument`

<!-- --8<-- [start:FirstOptionMatchableArgument] -->
```juvix
type FirstOptionMatchableArgument := mkFirstOptionMatchableArgument {
  data : Val;
};
```
<!-- --8<-- [end:FirstOptionMatchableArgument] -->

???+ quote "Arguments"

    `data`:
    : is the value of the matchable argument.

### `TemplateMatchableArgumentSecondOption SecondOptionMatchableArgument`

<!-- --8<-- [start:SecondOptionMatchableArgument] -->
```juvix
type SecondOptionMatchableArgument := mkSecondOptionMatchableArgument {
  data : String;
};
```
<!-- --8<-- [end:SecondOptionMatchableArgument] -->

???+ quote "Arguments"

    `data`:
    : is the value of the matchable argument.

### `TemplateMatchableArgument`

<!-- --8<-- [start:template-matchable-argument] -->
```juvix
type TemplateMatchableArgument :=
  | TemplateMatchableArgumentFirstOption FirstOptionMatchableArgument
  | TemplateMatchableArgumentSecondOption SecondOptionMatchableArgument
  ;
```
<!-- --8<-- [end:template-matchable-argument] -->

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
        TemplateMatchableArgument
        TemplateActionLabel
        TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateGuard] -->

    ### `TemplateGuardOutput`

    <!-- --8<-- [start:TemplateGuardOutput] -->
    ```juvix
    TemplateGuardOutput : Type :=
      GuardOutput
        TemplateMatchableArgument
        TemplateActionLabel
        TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateGuardOutput] -->

### `messageOneGuard`

<!-- --8<-- [start:messageOneGuard] -->
```juvix
messageOneGuard : TemplateGuard
  | _ _ :=  some (
    mkGuardOutput@{
      matchedArgs := [
        (TemplateMatchableArgumentSecondOption
          (mkSecondOptionMatchableArgument@{
            data := "Hello World!"
          })
        )
      ];
      actionLabel := TemplateActionLabelDoAlternative
        (left (TemplateActionLabelDoSomeThing "parameter 2"));
      precomputationTasks := [
        TemplatePrecomputationEntryCloseMailbox (
          mkCloseMailbox@{
            mailboxId := 1
          }
        );
        TemplatePrecomputationEntryDeleteMessage (
          mkDeleteMessage@{
              messageType := 1337;
              messageId := 0}
          )
        ]
      });
    ```
<!-- --8<-- [end:messageOneGuard] -->

## Action function

The action function amounts to one single case statement.

??? quote "Auxiliary Juvix code"

    ### `TemplateActionInput`

    <!-- --8<-- [start:TemplateActionInput] -->
    ```juvix
    TemplateActionInput : Type :=
      ActionInput
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateMatchableArgument
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
        TemplateMatchableArgument
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
          TemplateMatchableArgument
          TemplateActionLabel
          TemplatePrecomputationList;
    ```
    <!-- --8<-- [end:TemplateActionFunction] -->

### `doOneThingAction`

Give a short description of the action function.
This action does nothing.
It preserves the environment, produces no messages,
sets no timers, spawns no engines.

```juvix
doOneThingAction (input : TemplateActionInput) : TemplateActionEffect :=
  let
    env := ActionInput.env input;
    out := ActionInput.guardOutput input;
  in
    mkActionEffect@{
      newEnv := env;
      producedMessages := [];
      timers := [];
      spawnedEngines := [];
    }
```

### `someAction`

Give a short description of the action function.
This action does nothing.
It preserves the environment, produces no messages,
sets no timers, spawns no engines.

```juvix
someAction (input : TemplateActionInput) : TemplateActionEffect :=
  let
    env := ActionInput.env input;
    out := ActionInput.guardOutput input;
  in
    mkActionEffect@{
      newEnv := env;
      producedMessages := [];
      timers := [];
      spawnedEngines := [];
    }
```

### `templateAction`

Calls the action function corresponding to the action label set by the guard.

<!-- --8<-- [start:templateAction] -->
```juvix
templateAction (input : TemplateActionInput) : TemplateActionEffect :=
  let
    env := ActionInput.env input;
    out := ActionInput.guardOutput input;
  in
    case GuardOutput.actionLabel out of {
    | TemplateActionLabelDoOneThing := doOneThingAction input
    | TemplateActionLabelDoAlternative (left _) := someAction input
    | _ := undef
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
  Set TemplateMatchableArgument ->
  List (Set TemplateMatchableArgument)
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
    TemplateMatchableArgument
    TemplateActionLabel
    TemplatePrecomputationList;
```
<!-- --8<-- [end:TemplateBehaviour] -->

#### Instantiation

<!-- --8<-- [start:templateBehaviour] -->
```juvix
templateBehaviour : TemplateBehaviour :=
  mkEngineBehaviour@{
    guards := [messageOneGuard];
    action := templateAction;
    conflictSolver := templateConflictSolver;
  }
  ;
```
<!-- --8<-- [end:templateBehaviour] -->

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
        TemplateActionLabel
        TemplateActionArgument;
    ```
    <!-- --8<-- [end:TemplateGuard] -->

    ### `TemplateGuardOutput`

    <!-- --8<-- [start:TemplateGuardOutput] -->
    ```juvix
    TemplateGuardOutput : Type :=
      GuardOutput
        TemplateActionLabel
        TemplateActionArgument;
    ```
    <!-- --8<-- [end:TemplateGuardOutput] -->

    ### `TemplateActionSeq`

    <!-- --8<-- [start:TemplateActionSeq] -->
    ```juvix
    TemplateActionSeq : Type :=
      ActionSeq
        TemplateActionLabel;
    ```
    <!-- --8<-- [end:TemplateActionSeq] -->

### `justHiGuard`

<!-- --8<-- [start:justHiGuard] -->
```juvix
justHiGuard
  (t : TimestampedTrigger TemplateTimerHandle )
  (env : TemplateEnvironment) : Option TemplateGuardOutput :=
  case getMessageFromTimestampedTrigger t of {
  | some (MsgTemplate MsgTemplateJustHi) := some (
    mkGuardOutput@{
      actions := Action TemplateActionLabelDoNothing;
      args := [
        (TemplateActionArgumentTwo
          mkSecondArgument@{
            data := "Hello World!"
          })
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
      actions := Seq TemplateActionLabelExampleReply (Action TemplateActionLabelDoNothing);
      args := [];
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
        TemplateActionLabel
        TemplateActionArgument;
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
        TemplateActionLabel
        TemplateActionArgument;
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
          TemplateActionLabel
          TemplateActionArgument;
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
    case GuardOutput.args out of {
      | TemplateActionArgumentTwo (mkSecondArgument@{
          data := data;
        }) :: _ :=
        mkActionEffect@{
          env := env@EngineEnvironment{
            localState := mkTemplateLocalState@{
              taskQueue := mkCustomData@{
                word := data
              }
            }
          };
          msgs := [];
          timers := [];
          engines := [];
        }
      | _ := mkActionEffect@{
          env := env;
          msgs := [];
          timers := [];
          engines := [];
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
          env := env;
          msgs := [
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
          engines := [];
        }
      | _ := mkActionEffect@{
          env := env;
          msgs := [];
          timers := [];
          engines := [];
        }
    }
```

### `templateAction`

Calls the action function corresponding to the action label set by the guard.

<!-- --8<-- [start:templateAction] -->
```juvix
templateAction (label : TemplateActionLabel) (input : TemplateActionInput) : TemplateActionEffect :=
  case label of {
  | TemplateActionLabelDoNothing := doNothingAction input
  | TemplateActionLabelExampleReply := exampleReplyAction input
  };
```
<!-- --8<-- [end:templateAction] -->

## The Template behaviour

### `TemplateBehaviour`

<!-- --8<-- [start:TemplateBehaviour] -->
```juvix
TemplateBehaviour : Type :=
  EngineBehaviour
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateActionLabel
    TemplateActionArgument;
```
<!-- --8<-- [end:TemplateBehaviour] -->

#### Instantiation

<!-- --8<-- [start:templateBehaviour] -->
```juvix
templateBehaviour : TemplateBehaviour :=
  mkEngineBehaviour@{
    guards := [justHiGuard; exampleRequestGuard];
    action := templateAction;
  };
```
<!-- --8<-- [end:templateBehaviour] -->

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

```juvix
TemplateActionArguments : Type := List TemplateActionArgument;
```

## Guarded actions

??? quote "Auxiliary Juvix code"

    ### `TemplateGuard`

    <!-- --8<-- [start:TemplateGuard] -->
    ```juvix
    TemplateGuard : Type :=
      Guard
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments;
    ```
    <!-- --8<-- [end:TemplateGuard] -->

    ### `TemplateGuardOutput`

    <!-- --8<-- [start:TemplateGuardOutput] -->
    ```juvix
    TemplateGuardOutput : Type :=
      GuardOutput
        TemplateActionArguments;
    ```
    <!-- --8<-- [end:TemplateGuardOutput] -->

    ### `TemplateAction`

    <!-- --8<-- [start:TemplateAction] -->
    ```juvix
    TemplateAction : Type :=
      Action
          TemplateLocalState
          TemplateMailboxState
          TemplateTimerHandle
          TemplateActionArguments;
    ```
    <!-- --8<-- [end:TemplateActionFunction] -->

    ### `TemplateActionEffect`

    <!-- --8<-- [start:TemplateActionEffect] -->
    ```juvix
    TemplateActionEffect : Type :=
      ActionEffect
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments;
    ```
    <!-- --8<-- [end:TemplateActionEffect] -->

### `justHi`

#### `justHiGuard`

Guard description.

Condition
: Message type is `MsgTemplateJustHi`

<!-- --8<-- [start:justHiGuard] -->
```juvix
justHiGuard
  (tt : TemplateTimestampedTrigger)
  (env : TemplateEnvironment)
  : Option TemplateGuardOutput :=
  case getMessageFromTimestampedTrigger tt of {
  | some (MsgTemplate MsgTemplateJustHi) :=
    some mkGuardOutput@{
      args := [];
    }
  | _ := none
  };
```
<!-- --8<-- [end:justHiGuard] -->

#### `justHiAction`

Action description.

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
justHiAction
  (args : List TemplateActionArgument)
  (tt : TemplateTimestampedTrigger)
  (env : TemplateEnvironment)
  : Option TemplateActionEffect :=
  case args of {
  | TemplateActionArgumentTwo (mkSecondArgument@{
      data := data;
    }) :: _ :=
    some mkActionEffect@{
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
  | _ := none
  }
```

### `exampleReply`

#### `exampleReplyGuard`

Guard description.

Condition
: Message type is `MsgTemplateExampleRequest`

<!-- --8<-- [start:exampleRequestGuard] -->
```juvix
exampleReplyGuard
  (tt : TemplateTimestampedTrigger)
  (env : TemplateEnvironment)
  : Option TemplateGuardOutput :=
  let
    em := getEngineMsgFromTimestampedTrigger tt;
  in
    case em of {
    | some emsg :=
      case EngineMsg.msg emsg of {
      | MsgTemplate (MsgTemplateExampleRequest req) :=
        some mkGuardOutput@{
          args := [
            (TemplateActionArgumentTwo
              mkSecondArgument@{
                data := "Hello World!"
              })
          ];
        }
      | _ := none
      }
    | _ := none
    };
```
<!-- --8<-- [end:exampleRequestGuard] -->

#### `exampleReplyAction`

Action description.

State update
: The state remains unchanged.

Messages to be sent
: A `MsgTemplateExampleReply` message with `argOne` from the received `MsgTemplateExampleRequest`.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

```juvix
exampleReplyAction
  (args : List TemplateActionArgument)
  (tt : TemplateTimestampedTrigger)
  (env : TemplateEnvironment)
  : Option TemplateActionEffect :=
  let
    em := getEngineMsgFromTimestampedTrigger tt;
  in
    case em of {
    | some emsg :=
      case EngineMsg.msg emsg of {
      | MsgTemplate (MsgTemplateExampleRequest req) :=
        some mkActionEffect@{
          env := env;
          msgs := [
          mkEngineMsg@{
              sender := EngineMsg.sender emsg;
              target := EngineMsg.target emsg;
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
      | _ := none
      }
    | _ := none
  }
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
    TemplateActionArguments;
```
<!-- --8<-- [end:TemplateBehaviour] -->

#### Instantiation

<!-- --8<-- [start:templateBehaviour] -->
```juvix
templateBehaviour : TemplateBehaviour :=
  mkEngineBehaviour@{
    exec :=
      Seq (mkPair justHiGuard justHiAction)
      (Seq (mkPair exampleReplyGuard exampleReplyAction)
       End);
  };
```
<!-- --8<-- [end:templateBehaviour] -->

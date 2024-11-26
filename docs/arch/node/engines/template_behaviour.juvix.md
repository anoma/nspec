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
    import arch.node.engines.template_config open;
    import arch.node.engines.template_environment open;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;
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

<!-- --8<-- [start:TemplateActionArgument] -->
```juvix
type TemplateActionArgument :=
  | TemplateActionArgumentOne FirstArgument
  | TemplateActionArgumentTwo SecondArgument
  ;
```
<!-- --8<-- [end:TemplateActionArgument] -->

### `TemplateActionArguments`

<!-- --8<-- [start:TemplateActionArguments] -->
```juvix
TemplateActionArguments : Type := List TemplateActionArgument;
```
<!-- --8<-- [end:TemplateActionArguments] -->

## Actions

??? quote "Auxiliary Juvix code"

    ### `TemplateAction`

    <!-- --8<-- [start:TemplateAction] -->
    ```juvix
    TemplateAction : Type :=
      Action
        TemplateCfg
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:TemplateAction] -->

    ### `TemplateActionInput`

    <!-- --8<-- [start:TemplateActionInput] -->
    ```juvix
    TemplateActionInput : Type :=
      ActionInput
        TemplateCfg
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments
        Anoma.Msg;
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
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:TemplateActionEffect] -->

    ### `TemplateActionExec`

    <!-- --8<-- [start:TemplateActionExec] -->
    ```juvix
    TemplateActionExec : Type :=
      ActionExec
        TemplateCfg
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:TemplateActionExec] -->

### `justHiAction`

Action description.

State update
: Update state with the data set by `justHiGuard`.

Messages to be sent
: No messages are added to the send queue.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

Acquaintance updates
: None.

<!-- --8<-- [start:justHiAction] -->
```juvix
justHiAction
  (input : TemplateActionInput)
  : Option TemplateActionEffect :=
  let
    args := ActionInput.args input;
    env := ActionInput.env input;
  in
    case args of {
    | TemplateActionArgumentTwo (mkSecondArgument@{
        data := data;
      }) :: _ :=
      some mkActionEffect@{
        env := env@EngineEnv{
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
<!-- --8<-- [end:justHiAction] -->

#### `exampleReplyAction`

Respond with a `TemplateMsgExampleResponse`.

State update
: The state remains unchanged.

Messages to be sent
: A `TemplateMsgExampleReply` message with the data set by `exampleReplyGuard`.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

<!-- --8<-- [start:exampleReplyAction] -->
```juvix
exampleReplyAction
  (input : TemplateActionInput)
  : Option TemplateActionEffect :=
  let
    args := ActionInput.args input;
    cfg := ActionInput.cfg input;
    env := ActionInput.env input;
    trigger := ActionInput.trigger input;
    emsg := getEngineMsgFromTimestampedTrigger trigger;
  in
    case emsg of {
    | some mkEngineMsg@{
        msg := Anoma.MsgTemplate (TemplateMsgExampleRequest req);
        sender := sender;
        target := target;
        mailbox := mailbox;
      } :=
      some mkActionEffect@{
        env := env;
        msgs := [
        mkEngineMsg@{
          sender := getEngineIDFromEngineCfg cfg;
          target := sender;
            mailbox := some 0;
            msg :=
              Anoma.MsgTemplate
                (TemplateMsgExampleReply
                  (ok mkExampleReplyOk@{
                    argOne := ExampleRequest.argOne req;
                  }));
          }
        ];
        timers := [];
        engines := [];
      }
  | _ := none
  };
```
<!-- --8<-- [end:exampleReplyAction] -->

## Action Labels

### `justHiActionLabel`

```juvix
justHiActionLabel : TemplateActionExec := Seq [ justHiAction ];
```

### `exampleReplyActionLabel`

```juvix
exampleReplyActionLabel : TemplateActionExec := Seq [ exampleReplyAction ];
```

### `doBothActionLabel`

```juvix
doBothActionLabel : TemplateActionExec :=
  Seq [
    justHiAction;
    exampleReplyAction;
  ];
```

## Guards

??? quote "Auxiliary Juvix code"

    ### `TemplateGuard`

    <!-- --8<-- [start:TemplateGuard] -->
    ```juvix
    TemplateGuard : Type :=
      Guard
        TemplateCfg
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:TemplateGuard] -->

    ### `TemplateGuardOutput`

    <!-- --8<-- [start:TemplateGuardOutput] -->
    ```juvix
    TemplateGuardOutput : Type :=
      GuardOutput
        TemplateCfg
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:TemplateGuardOutput] -->

    ### `TemplateGuardEval`

    <!-- --8<-- [start:TemplateGuardEval] -->
    ```juvix
    TemplateGuardEval : Type :=
      GuardEval
        TemplateCfg
        TemplateLocalState
        TemplateMailboxState
        TemplateTimerHandle
        TemplateActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:TemplateGuardEval] -->

### `justHiGuard`

Guard description (optional).

Condition
: Message type is `TemplateMsgJustHi`.

<!-- --8<-- [start:justHiGuard] -->
```juvix
justHiGuard
  (trigger : TemplateTimestampedTrigger)
  (cfg : EngineCfg TemplateCfg)
  (env : TemplateEnv)
  : Option TemplateGuardOutput :=
  let
    emsg := getEngineMsgFromTimestampedTrigger trigger;
  in
    case emsg of {
    | some mkEngineMsg@{
        msg := Anoma.MsgTemplate TemplateMsgJustHi;
      } :=
      some mkGuardOutput@{
        action := justHiActionLabel;
        args := [
          (TemplateActionArgumentTwo
            mkSecondArgument@{
              data := "Hello World!"
            })
        ];
      }
    | _ := none
    };
```
<!-- --8<-- [end:justHiGuard] -->

### `exampleReplyGuard`

Guard description (optional).

Condition
: Message type is `TemplateMsgExampleRequest`.

<!-- --8<-- [start:exampleReplyGuard] -->
```juvix
exampleReplyGuard
  (tt : TemplateTimestampedTrigger)
  (cfg : EngineCfg TemplateCfg)
  (env : TemplateEnv)
  : Option TemplateGuardOutput :=
  let
    emsg := getEngineMsgFromTimestampedTrigger tt;
  in
    case emsg of {
    | some mkEngineMsg@{
        msg := Anoma.MsgTemplate (TemplateMsgExampleRequest req);
        sender := mkPair none _; -- from local engines only (NodeID is none)
        target := target;
        mailbox := mailbox;
      } :=
      some mkGuardOutput@{
        action := exampleReplyActionLabel;
        args := [];
      }
    | _ := none
    };
```
<!-- --8<-- [end:exampleReplyGuard] -->

## The Template behaviour

### `TemplateBehaviour`

<!-- --8<-- [start:TemplateBehaviour] -->
```juvix
TemplateBehaviour : Type :=
  EngineBehaviour
    TemplateCfg
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:TemplateBehaviour] -->

#### Instantiation

<!-- --8<-- [start:templateBehaviour] -->
```juvix
templateBehaviour : TemplateBehaviour :=
  mkEngineBehaviour@{
    guards :=
      First [
        justHiGuard;
        exampleReplyGuard;
      ];
  };
```
<!-- --8<-- [end:templateBehaviour] -->

## Diagrams

### `justHi`

<figure markdown>

```mermaid
flowchart TD
  CM>TemplateMsgJustHi]
  A(justHiAction)
  ES[(State update)]

  CM --justHiGuard--> A --justHiActionLabel--> ES
```

<figcaption>`justHi` flowchart</figcaption>
</figure>

### `exampleReply`

<figure markdown>

```mermaid
flowchart TD
  CM>TemplateMsgExampleRequest]
  CS[(State condition)]
  A(exampleReplyAction)
  ES[(State update)]
  EM>TemplateMsgExampleResponse]

  CS & CM --exampleReplyGuard--> A --exampleReplyActionLabel--> ES & EM
```

<figcaption>`exampleReply` flowchart</figcaption>
</figure>

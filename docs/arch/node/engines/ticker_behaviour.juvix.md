---
icon: material/animation-play
search:
  exclude: false
categories:
- engine
- node
tags:
- ticker-engine
- engine-behaviour
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.ticker_behaviour;

    import arch.node.engines.ticker_messages open;
    import arch.node.engines.ticker_environment open;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.engine open;
    import arch.node.types.anoma open;
    ```

# Ticker Behaviour

## Overview

The Ticker engine maintains a counter as local state and allows two actions:
incrementing the counter and sending the current counter value.

## Action arguments

### `TickerActionArgumentReplyTo ReplyTo`

```juvix
type ReplyTo := mkReplyTo {
  whoAsked : Option EngineID;
  mailbox : Option MailboxID;
};
```

This action argument contains the address and mailbox ID of where the
response message should be sent.

`whoAsked`:
: is the address of the engine that sent the message.

`mailbox`:
: is the mailbox ID where the response message should be sent.

### `TickerActionArgument`

<!-- --8<-- [start:TickerActionArgument] -->
```juvix
type TickerActionArgument :=
  | TickerActionArgumentReplyTo ReplyTo
  ;
```
<!-- --8<-- [end:TickerActionArgument] -->

### `TickerActionArguments`

<!-- --8<-- [start:ticker-action-arguments] -->
```juvix
TickerActionArguments : Type := List TickerActionArgument;
```
<!-- --8<-- [end:ticker-action-arguments] -->

## Guarded actions

??? quote "Auxiliary Juvix code"

    ### TickerGuard

    <!-- --8<-- [start:TickerGuard] -->
    ```juvix
    TickerGuard : Type :=
      Guard
        TickerLocalState
        TickerTimerHandle
        TickerMailboxState
        TickerActionArguments;
    ```
    <!-- --8<-- [end:TickerGuard] -->

    ### TickerGuardOutput

    <!-- --8<-- [start:TickerGuardOutput] -->
    ```juvix
    TickerGuardOutput : Type :=
      GuardOutput
        TickerActionArguments;
    ```
    <!-- --8<-- [end:TickerGuardOutput] -->

    ### `TickerAction`

    ```juvix
    TickerAction : Type :=
      Action
        TickerLocalState
        TickerMailboxState
        TickerTimerHandle
        TickerActionArguments;
    ```

    ### `TickerActionEffect`

    ```juvix
    TickerActionEffect : Type :=
      ActionEffect
        TickerLocalState
        TickerMailboxState
        TickerTimerHandle
        TickerActionArguments;
    ```

### `increment`

<figure markdown>

```mermaid
flowchart TD
  CM>TickerMsgIncrement]
  A(incrementAction)
  ES[(increment counter)]

  CM --> A --> ES
```

<figcaption>increment flowchart</figcaption>
</figure>

#### `incrementGuard`

Condition
: Message type is `TickerMsgIncrement`.

<!-- --8<-- [start:incrementGuard] -->
```juvix
incrementGuard
  (tt : TimestampedTrigger TickerTimerHandle )
  (env : TickerEnvironment)
  : Option TickerGuardOutput :=
  let
    emsg := getEngineMsgFromTimestampedTrigger tt;
  in
    case emsg of {
    | some mkEngineMsg@{
        msg := (MsgTicker TickerMsgIncrement);
      } :=
    some mkGuardOutput@{
      args := [];
    }
  | _ := none
  };
```
<!-- --8<-- [end:incrementGuard] -->

#### `incrementAction`

Increment the counter.

State update
: The counter value is increased by one.

Messages to be sent
: No messages are added to the send queue.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

```juvix
incrementAction
  (args : List TickerActionArgument)
  (tt : TickerTimestampedTrigger)
  (env : TickerEnvironment)
  : Option TickerActionEffect :=
  let
    counterValue := TickerLocalState.counter (EngineEnv.localState env)
  in
    some mkActionEffect@{
      env := env@EngineEnv{
        localState := mkTickerLocalState@{
          counter := counterValue + 1
        }
      };
      msgs := [];
      timers := [];
      engines := [];
    }
```

### `countReply`

<figure markdown>

```mermaid
flowchart TD
  CM>TemplateMsgCountRequest]
  A(countAction)
  EM>TemplateMsgCountReply]

  CM --> A --> EM
```

<figcaption>`countReply` flowchart</figcaption>
</figure>

#### `countReplyGuard`

Condition
: Message type is `TickerMsgCountRequest`.

<!-- --8<-- [start:countGuard] -->
```juvix
countReplyGuard
  (tt : TimestampedTrigger TickerTimerHandle)
  (env : TickerEnvironment)
  : Option TickerGuardOutput :=
  let
    emsg := getEngineMsgFromTimestampedTrigger tt;
  in
    case emsg of {
    | some mkEngineMsg@{
        msg := MsgTicker TickerMsgCount;
      } :=
      some mkGuardOutput@{
        args := [];
      }
    | _ := none
    };
```
<!-- --8<-- [end:countGuard] -->

#### `countReplyAction`

Respond with the counter value.

State update
: The state remains unchanged.

Messages to be sent
: A message with the current counter value is sent to the requester.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

```juvix
countReplyAction
  (args : List TickerActionArgument)
  (tt : TickerTimestampedTrigger)
  (env : TickerEnvironment)
  : Option TickerActionEffect :=
  let
    em := getEngineMsgFromTimestampedTrigger tt;
    counterValue := TickerLocalState.counter (EngineEnv.localState env)
  in
    case em of {
    | some emsg :=
      some mkActionEffect@{
        env := env;
        msgs := [
          mkEngineMsg@{
            sender := mkPair (some (EngineEnv.node env)) (some (EngineEnv.name env));
            target := EngineMsg.sender emsg;
            mailbox := some 0;
            msg :=
              MsgTicker
                (TickerMsgCountReply
                  mkCountReply@{
                    counter := counterValue;
                  })
          }
        ];
        timers := [];
        engines := [];
      }
    | _ := none
    };
```

## The Ticker behaviour

### `TickerBehaviour`

<!-- --8<-- [start:TickerBehaviour] -->
```juvix
TickerBehaviour : Type :=
  EngineBehaviour
    TickerLocalState
    TickerMailboxState
    TickerTimerHandle
    TickerActionArguments;
```
<!-- --8<-- [end:TickerBehaviour] -->

#### Instantiation

<!-- --8<-- [start:TickerBehaviour-instance] -->
```juvix
tickerBehaviour : TickerBehaviour :=
  mkEngineBehaviour@{
    exec :=
      Seq [(mkPair incrementGuard incrementAction);
           (mkPair countReplyGuard countReplyAction)]
      End;
  };
```
<!-- --8<-- [end:TickerBehaviour-instance] -->

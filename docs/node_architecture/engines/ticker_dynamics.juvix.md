---
icon: octicons/project-template-24
search:
  exclude: false
tags:
  - engine-family
  - example
  - ticker
  - Juvix
---

??? warning "under sconstruction"

    This page is still under construction, needs to be updated with the latest
    changes in the engine family type.

??? info "Juvix imports"

    ```juvix
    module node_architecture.engines.ticker_dynamics;

    import node_architecture.basics open;
    import node_architecture.types.engine_family open;
    import node_architecture.engines.ticker_environment open public;
    ```

# Ticker Dynamics

## Overview

A ticker has a counter as local state and allows to perform two actions:

- Incrementing the counter.
- Sending the current counter value.

The increment is in response to an `Increment`-message
and the sending of the value is in response to a `Count`-message.

## Action labels

```juvix
type GuardReturnLabel :=
  | doIncrement
  | doRespond Nat
;
```

### doIncrement

This action increments the counter.

### doRespond

Return the current value of the counter.

## Matchable arguments

The only argument that is worth fetching is the address and
mailbox ID of where the message is to be sent to.

```juvix
type GuardReturnArgs :=
  | ReplyTo (Maybe Address) (Maybe MailboxID);
```

## Precomputation results

There are no non-trivial pre-computations.

```juvix
type GuardReturnOther :=
  | nuthing ;
```

<!--
Regarding the guard function's return type, we must return two different types
of values. The first value is a boolean (or possibly Unit) that indicates if the
guard condition is met. The second value is the name of the message sender,
which is used to set the target for the resulting message with the counted
value.
-->

## Guarded actions

### doIncrementIfIncrement

#### Purpose

The guard of doIncrementIfIncrement is enabled
if the trigger is an `Increment`-message;
the action increments the counter.

#### Guard ifIncrement

The `ifIncrement` guard checks whether
an increment message arrives.

```mermaid
flowchart TD
    C{Increment <br> message <br> received ?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([doIncrement])
```

```juvix
ifIncrement : (Maybe Time)
      -> (Trigger TickerMessage TickerTimerHandle)
      -> (EngineEnvironment TickerLocalState TickerMessage TickerMailboxState TickerTimerHandle)
      -> Maybe (GuardOutput GuardReturnArgs GuardReturnLabel GuardReturnOther)
:= \{
      | _ (MessageArrived@{ envelope := m}) _ :=
          case getMessageType m of {
            | Increment := just (  mkGuardOutput@{
                args := [];
                label := doIncrement;
                other := nuthing;
              }
            )
            | _ := nothing
          }
      | _ (Elapsed@{ timers := ts }) _ := nothing
      };
```

#### doIncrement

This is the only action label and it increments the counter.

!!! todo "Continue here"

    make the code work

```
performIncrement : ActionInput TickerLocalState TickerMessage TickerMailboxState TickerTimerHandle GuardReturnArgs GuardReturnLabel GuardReturnOther
                 -> Maybe (ActionResult TickerLocalState TickerMessage TickerMailboxState TickerTimerHandle GuardReturnArgs GuardReturnLabel GuardReturnOther TickerProtocolMessage TickerProtocolEnvironment)
                 := \{
                  | (mkActionInput@{ env := previousEnv }) :=
                  let counterValue := previousEnv
                  in
                  just  counterValue
};
```

```
| (mkActionInput@{ env := previousEnv }) :=

            mkActionResult@{
              newEnv := previousEnv@EngineEnvironment{
                localState := mkLocalStateType@{
                  counter := counterValue + 1
                }| (mkActionInput@{ env := previousEnv }) :=
            let counterValue := LocalStateType.counter (localState previousEnv)
            in
            mkActionResult@{
              newEnv := previousEnv@EngineEnvironment{
                localState := mkLocalStateType@{
                  counter := counterValue + 1
                }
```

##### State update

The counter value is increased by one.

##### Messages to be sent

No messages need to be sent.

##### Engines to be created

No new engines need to be created.

##### Timers to be set/cancelled/reset

Timers are unchanged.



On the other hand, the Ticker engine does not require to create any
engine instance, therefore, the `SpawnEngineType` is set to `Unit`.

```juvix
syntax alias SpawnEngineType := Unit;
```

Therefore, the `GuardedAction` type is defined as follows:

```
GuardedActionType : Type :=
  GuardedAction
    TickerLocalState
    TickerMessage
    TickerMailboxState
    TickerTimerHandle
    GuardReturnArgs
    GuardReturnLabel
    GuardReturnOther
    TickerProtocolMessage
    TickerProtocolEnvironment;
```

## Guarded Action: Increment Counter

This action increments the counter upon receiving an `Increment` message.

```
incrementCounter : GuardedActionType := mkGuardedAction@{
  guard := \{
      | _ (MessageArrived@{ envelope := m}) _ :=
          case getMessageType m of {
            | Increment := just (IncrementGuard true)
            | _ := nothing
          }
      | _ (Elapsed@{ timers := ts }) _ := nothing
      };
  action := \{
      | (mkActionInput@{ env := previousEnv }) :=
            let counterValue := LocalStateType.counter (localState previousEnv)
            in
            mkActionResult@{
              newEnv := previousEnv@EngineEnvironment{
                localState := mkLocalStateType@{
                  counter := counterValue + 1
                }
              };
          producedMessages := [];
          spawnedEngines := [];
          timers := [];
        }
      }
};
```

## Guarded Action: Respond with Counter

This action sends the current counter value upon receiving a `Count` message.

```
respondWithCounter : GuardedActionType := mkGuardedAction@{
  guard :=
    \{
      | _ (Elapsed@{ timers := ts }) state := nothing
      | _ (MessageArrived@{ envelope := m }) state :=
          case getMessageType m of {
            | Count := just (RespondGuard (getMessageSender m))
            | _ := nothing
          }
      };
  action := \{ (mkActionInput@{
            guardOutput := senderRef ;
            env := previousEnv }) :=
            let lState := (localState previousEnv);
                counterValue := LocalStateType.counter lState;
                sender := case senderRef of {
                | (RespondGuard s) := Left s
                | _ := Right 0 -- no address
                };
                in
            mkActionResult@{
              newEnv := previousEnv; -- nothing changes
              producedMessages := [
                    mkEnvelopedMessage@{
                        packet := mkMessagePacket@{
                          target := sender;
                          message := mkMessage@{
                            messageType := Result counterValue;
                            payload := natToString counterValue
                          }
                        };
                        sender := name previousEnv
                      }
              ];
              spawnedEngines := [];
              timers := [];
            }
      }
};
```


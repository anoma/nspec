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

!!! warning

    This page is still under construction, needs to be updated with the latest
    changes in the engine family type.

??? info "Juvix imports"

    ```juvix
    module tutorial.engines.examples.ticker_dynamics;

    import node_architecture.basics open;
    import node_architecture.types.engine_family as EngineFamily;
    open EngineFamily using {
        Engine;
        EngineEnvironment;
        EngineFamily;
        mkActionInput;
        mkActionResult;
        mkEngine;
        mkEngineEnvironment;
        mkEngineFamily;
        mkGuardedAction
    };
    open EngineFamily.EngineEnvironment;
    import tutorial.engines.examples.ticker_environment open public;
    import tutorial.engines.examples.ticker_protocol_types open;
    ```

# Ticker Guarded Actions

- Incrementing the counter.
- Responding with the counter value.

Regarding the guard function's return type, we must return two different types
of values. The first value is a boolean (or possibly Unit) that indicates if the
guard condition is met. The second value is the name of the message sender,
which is used to set the target for the resulting message with the counted
value.

```juvix
type GuardReturnArgsType :=
  | IncrementGuard Bool
  | RespondGuard Name;
```

```juvix
syntax alias GuardReturnLabelType := Unit;
syntax alias GuardReturnOtherType := Unit;
```

On the other hand, the Ticker engine does not require to create any
engine instance, therefore, the `SpawnEngineType` is set to `Unit`.

```juvix
syntax alias SpawnEngineType := Unit;
```

Therefore, the `GuardedAction` type is defined as follows:

```juvix
GuardedActionType : Type :=
  EngineFamily.GuardedAction
    TickerLocalState
    TickerMessage
    TickerMailboxState
    TickerTimerHandle
    GuardReturnArgsType
    GuardReturnLabelType
    GuardReturnOtherType
    TickerProtocolMessage
    TickerProtocolEnvironment;
```

## Guarded Action: Increment Counter

This action increments the counter by 1 upon receiving an `Increment` message.

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


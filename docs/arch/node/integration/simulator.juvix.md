---
icon: material/play
search:
  exclude: false
  boost: 2
tags:
  - work-in-progress
  - simulator
  - engine
---

# Engine Simulator

## Module Setup and Core Types

The main simulator module with essential imports and the message selection strategy type definition.

??? code "Juvix imports"

    ```juvix
    module arch.node.integration.simulator;

    import prelude open;
    open OMap;
    import arch.node.types.basics open public;
    import arch.node.types.messages open public;
    import arch.node.types.identities open;
    import arch.node.types.engine_config open public;
    import arch.node.types.engine_environment open;
    import arch.node.types.engine_behaviour open;
    import arch.node.types.engine open public;
    import arch.node.types.anoma_engines open;
    import arch.node.types.anoma_message open;
    import arch.node.types.anoma_config open;
    import arch.node.types.anoma_environment open;
    ```

```juvix
-- Type for message selection strategy
MessageSelector : Type :=
  (messages : List (EngineMsg Msg)) ->
  Option (Pair (EngineMsg Msg) (List (EngineMsg Msg)));
```

```juvix
-- Example selector that takes the first message in the list
selectFirstMessage (messages : List (EngineMsg Msg)) : Option (Pair (EngineMsg Msg) (List (EngineMsg Msg))) :=
  case messages of {
    | [] := none
    | msg :: rest := some (mkPair msg rest)
  };
```

## Network and Node State Types

Data structures for representing nodes, network state, and the overall simulation environment.

```juvix
-- Node type that contains a map from engine names to engines
type Node := mkNode@{
  engines : OMap EngineName Eng;
};
```

```juvix
-- Network state contains all nodes, in-transit messages, and current time
type NetworkState := mkNetworkState@{
  nodes : OMap NodeID Node;
  messages : List (EngineMsg Msg);
  currentTime : Time;
  incrementId : NodeID -> NodeID;
  nextId : NodeID;
};
```

## Guard Execution and Action Processing

Core logic for executing guard outputs and processing engine actions based on triggers.

```juvix
-- Helper function to execute a guard output
executeGuardOutput
  {C S B H A AM AC AE : Type}
  (output : GuardOutput C S B H A AM AC AE)
  (eng : Engine C S B H A AM AC AE)
  (trigger : TimestampedTrigger H AM)
  : Option (ActionEffect S B H AM AC AE) :=
  case output of {
    | GuardOutput.mk@{action := ActionExec.Seq actions; args := args} :=
      let
        -- Execute each action in sequence
        terminating
        executeAction (acts : List (Action C S B H A AM AC AE)) (currentEnv : EngineEnv S B H AM) : Option (ActionEffect S B H AM AC AE) :=
          case acts of {
            | [] := none
            | act :: rest :=
              case act (ActionInput.mk@{
                args := args;
                cfg := Engine.cfg eng;
                env := currentEnv;
                trigger := trigger
              }) of {
                | none := executeAction rest currentEnv
                | some effect :=
                  case executeAction rest (ActionEffect.env effect) of {
                    | none := some effect
                    | some nextEffect := some ActionEffect.mk@{
                        env := ActionEffect.env nextEffect;
                        msgs := ActionEffect.msgs effect ++ ActionEffect.msgs nextEffect;
                        timers := ActionEffect.timers effect ++ ActionEffect.timers nextEffect;
                        engines := ActionEffect.engines effect ++ ActionEffect.engines nextEffect
                      }
                  }
              }
          };
      in executeAction actions (Engine.env eng)
  };
```

## Engine Evaluation and Execution

Functions for evaluating guards and executing actions for specific engines, including both typed and untyped variants.

```juvix
-- Helper function to evaluate guards and execute actions for a specific engine type
terminating
evaluateAndExecute
  {C S B H A AM AC AE : Type}
  (eng : Engine C S B H A AM AC AE)
  (msg : EngineMsg AM)
  : Option (Pair (List (EngineMsg AM)) (Pair (List (Pair AC AE)) (Engine C S B H A AM AC AE))) :=
  let
    -- Create a trigger from the message
    trigger := TimestampedTrigger.mkTimestampedTrigger@{
      time := right 0;  -- Dummy time value for now
      trigger := Trigger.MessageArrived@{msg := msg}
    };
    -- Get the engine's behaviour
    behaviour := Engine.behaviour eng;
    -- Evaluate guards based on strategy
    guardResult := case EngineBehaviour.guards behaviour of {
      | GuardEval.First guards :=
        let
          -- Try each guard until one matches
          terminating
          tryGuard (gs : List (Guard C S B H A AM AC AE)) : Option (GuardOutput C S B H A AM AC AE) :=
            case gs of {
              | [] := none
              | g :: rest :=
                case g trigger (Engine.cfg eng) (Engine.env eng) of {
                  | none := tryGuard rest
                  | some output := some output
                }
            };
        in tryGuard guards
      | GuardEval.Any guards := -- What's this actually supposed to do?
        let
          -- Try each guard until one matches
          terminating
          tryGuard (gs : List (Guard C S B H A AM AC AE)) : Option (GuardOutput C S B H A AM AC AE) :=
            case gs of {
              | [] := none
              | g :: rest :=
                case g trigger (Engine.cfg eng) (Engine.env eng) of {
                  | none := tryGuard rest
                  | some output := some output
                }
            };
        in tryGuard guards
    };
    -- If a guard matched, execute its action
    actionResult := case guardResult of {
      | none := none
      | some output := executeGuardOutput output eng trigger
    };
    -- If an action was executed, update the engine with the new environment
    updatedEngine := case actionResult of {
      | none := none
      | some effect := some (eng@Engine{env := ActionEffect.env effect})
    };
  in case updatedEngine of {
    | none := none
    | some newEng := case actionResult of {
      | none := none -- Should this be all or nothing, like it is?
      | some effect := some (mkPair (ActionEffect.msgs effect) (mkPair (ActionEffect.engines effect) newEng))
    }
  };
```

## Engine Dispatcher

The large dispatcher function that handles evaluation and execution for all engine types in the system.

```juvix
-- Helper function to evaluate and execute for any engine type
evaluateAndExecuteEng (eng : Eng) (msg : EngineMsg Msg) : Option (Pair (List (EngineMsg Msg)) (Pair (List (Pair Cfg Env)) Eng)) :=
  case eng of {
    | Eng.IdentityManagement e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.IdentityManagement newEng)))
    }
    | Eng.Decryption e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Decryption newEng)))
    }
    | Eng.Encryption e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Encryption newEng)))
    }
    | Eng.Commitment e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Commitment newEng)))
    }
    | Eng.Verification e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Verification newEng)))
    }
    | Eng.ReadsFor e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.ReadsFor newEng)))
    }
    | Eng.SignsFor e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.SignsFor newEng)))
    }
    | Eng.Naming e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Naming newEng)))
    }
    | Eng.LocalKeyValueStorage e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.LocalKeyValueStorage newEng)))
    }
    | Eng.Logging e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Logging newEng)))
    }
    | Eng.WallClock e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.WallClock newEng)))
    }
    | Eng.LocalTSeries e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.LocalTSeries newEng)))
    }
    | Eng.Router e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Router newEng)))
    }
    | Eng.TransportProtocol e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.TransportProtocol newEng)))
    }
    | Eng.TransportConnection e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.TransportConnection newEng)))
    }
    | Eng.PubSubTopic e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.PubSubTopic newEng)))
    }
    | Eng.Storage e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Storage newEng)))
    }
    | Eng.MempoolWorker e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.MempoolWorker newEng)))
    }
    | Eng.Executor e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Executor newEng)))
    }
    | Eng.Shard e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Shard newEng)))
    }
    | Eng.Ticker e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Ticker newEng)))
    }
    | Eng.Template e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.Template newEng)))
    }
    | Eng.TemplateMinimum e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (Eng.TemplateMinimum newEng)))
    }
  };
```

## Network State Management

Functions for managing network state updates, including adding new engines and updating existing ones.

```juvix
-- Helper function to add a single new engine to a node
addNewEngine (state : NetworkState) (nodeId : NodeID) (cfg : Cfg) (env : Env) : NetworkState :=
  case OMap.lookup nodeId (NetworkState.nodes state) of {
    | none := state
    | some node :=
      case mkEng nodeId (mkPair cfg env) of {
        | none := state
        | some (mkPair newEng newEngineId) :=
          let
            engineName := snd newEngineId;
            updatedNode := node@Node{engines := OMap.insert engineName newEng (Node.engines node)};
          in state@NetworkState{
            nodes := OMap.insert nodeId updatedNode (NetworkState.nodes state)
          }
      }
  };
```

```juvix
-- Helper function to update an engine's state, add new messages, and create new engines
updateNetworkState (state : NetworkState) (target : EngineID) (eng : Eng) (msgs : List (EngineMsg Msg)) (cfgEnvPairs : List (Pair Cfg Env)) : NetworkState :=
  let
    -- Get the node ID from the target engine ID
    nodeId := case target of {
      | mkPair none _ := none
      | mkPair (some nid) _ := some nid
    };
    -- Get the engine name from the target engine ID
    engineName := snd target;
    -- Look up the target node and update it
    state' := case nodeId of {
      | none := state
      | some nid := case OMap.lookup nid (NetworkState.nodes state) of {
        | none := state
        | some n := state@NetworkState{
            nodes := OMap.insert nid (n@Node{engines := OMap.insert engineName eng (Node.engines n)}) (NetworkState.nodes state)
          }
      }
    };
    -- Then fold over the config/env pairs to create new engines in the target node
    stateWithMessages := state'@NetworkState{messages := NetworkState.messages state ++ msgs};
    finalState := foldl
      (\{s (mkPair cfg env) := case nodeId of {
        | none := s
        | some nid := addNewEngine s nid cfg env
      }})
      stateWithMessages
      cfgEnvPairs
  in finalState;
```

## Core Simulation Logic

The main step function and simulation loops for processing messages and running the simulation.

```juvix
-- Step function that processes one message and updates network state
step (selector : MessageSelector) (state : NetworkState) : Pair NetworkState (Option (EngineMsg Msg)) :=
  let
    -- Try to select a message using the selector
    selected := selector (NetworkState.messages state);
  in case selected of {
    | none := mkPair state none
    | some (mkPair msg rest) :=
      let
        state' := state@NetworkState{messages := rest};
        -- Get the target engine ID from the message
        target := EngineMsg.target msg;
        -- Get the node ID and engine name from the target engine ID
        nodeId := case target of {
          | mkPair none _ := none
          | mkPair (some nid) _ := some nid
        };
        engineName := snd target;
        -- Look up the target engine
        engine := case nodeId of {
          | none := none
          | some nid := case OMap.lookup nid (NetworkState.nodes state) of {
            | none := none
            | some n := OMap.lookup engineName (Node.engines n)
          }
        };
      in case engine of {
        | none := mkPair state' none  -- Target engine not found, remove message and return state
        | some eng :=
          let
            -- Try to evaluate and execute for the engine
            result := evaluateAndExecuteEng eng msg;
          in case result of {
            | none := mkPair state' none  -- No action to execute, remove message and return state
            | some (mkPair msgs (mkPair cfgEnvPairs newEng)) :=
              mkPair (updateNetworkState state' target newEng msgs cfgEnvPairs) (some msg)
          }
      }
  };
```

```juvix
-- Simulate function that runs for a specified number of steps and collects successfully delivered messages
terminating
simulate (selector : MessageSelector) (state : NetworkState) (steps : Nat) : List (EngineMsg Msg) :=
  case steps of {
    | zero := []
    | suc n :=
      let
        -- Apply one step
        nextPair := step selector state;
        newState := fst nextPair;
        processedMsgOpt := snd nextPair;
        -- Recursively simulate remaining steps
        restMsgs := simulate selector newState n;
      in case processedMsgOpt of {
        | none := restMsgs
        | some processedMsg := processedMsg :: restMsgs
      }
  };
```

```juvix
-- Simulate function that runs for a specified number of steps and collects both
-- successfully delivered and failed messages.
terminating
simulateWithFailures
  (selector : MessageSelector)
  (state : NetworkState)
  (steps : Nat)
  : Pair (List (EngineMsg Msg)) (List (EngineMsg Msg)) :=
  case steps of {
    | zero := mkPair [] []
    | suc n :=
      let
        -- Try to select a message using the selector
        selected := selector (NetworkState.messages state);
      in case selected of {
        | none := -- No message selected, continue simulation
          let
            -- Recursively simulate remaining steps
            recursiveResult := simulateWithFailures selector state n;
          in recursiveResult
        | some (mkPair msg rest) := -- Message selected
          let
            state' := state@NetworkState{messages := rest};
            -- Apply one step for the selected message
            nextPair := step selector state; -- Need to use the original state here for step
            newState := fst nextPair;
            processedMsgOpt := snd nextPair;
            -- Recursively simulate remaining steps with the new state
            recursiveResult := simulateWithFailures selector newState n;
            successMsgs := fst recursiveResult;
            failedMsgs := snd recursiveResult;
          in case processedMsgOpt of {
            | none := -- Message failed to deliver
              mkPair successMsgs (msg :: failedMsgs)
            | some processedMsg := -- Message delivered successfully
              mkPair (processedMsg :: successMsgs) failedMsgs
          }
      }
  };
```

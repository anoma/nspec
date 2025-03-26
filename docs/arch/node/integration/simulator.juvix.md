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

```juvix
module arch.node.integration.simulator;

import prelude open;
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

-- Type for message selection strategy
MessageSelector : Type :=
  (messages : List (EngineMsg Msg)) ->
  Option (Pair (EngineMsg Msg) (List (EngineMsg Msg)));

-- Example selector that takes the first message in the list
selectFirstMessage (messages : List (EngineMsg Msg)) : Option (Pair (EngineMsg Msg) (List (EngineMsg Msg))) :=
  case messages of {
    | [] := none
    | msg :: rest := some (mkPair msg rest)
  };

-- Network state contains all engines, in-transit messages, and current time
type NetworkState := mkNetworkState@{
  engines : Map EngineID Eng;
  messages : List (EngineMsg Msg);
  currentTime : Time;
  incrementId : NodeID -> NodeID;
  nextId : NodeID;
};

-- Helper function to execute a guard output
executeGuardOutput
  {C S B H A AM AC AE : Type}
  (output : GuardOutput C S B H A AM AC AE)
  (eng : Engine C S B H A AM AC AE)
  (trigger : TimestampedTrigger H AM)
  : Option (ActionEffect S B H AM AC AE) :=
  case output of {
    | mkGuardOutput@{action := Seq actions; args := args} :=
      let
        -- Execute each action in sequence
        terminating
        executeAction (acts : List (Action C S B H A AM AC AE)) (currentEnv : EngineEnv S B H AM) : Option (ActionEffect S B H AM AC AE) :=
          case acts of {
            | [] := none
            | act :: rest :=
              case act (mkActionInput@{
                args := args;
                cfg := Engine.cfg eng;
                env := currentEnv;
                trigger := trigger
              }) of {
                | none := executeAction rest currentEnv
                | some effect :=
                  case executeAction rest (ActionEffect.env effect) of {
                    | none := some effect
                    | some nextEffect := some mkActionEffect@{
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

-- Helper function to evaluate guards and execute actions for a specific engine type
terminating
evaluateAndExecute
  {C S B H A AM AC AE : Type}
  (eng : Engine C S B H A AM AC AE)
  (msg : EngineMsg AM)
  : Option (Pair (List (EngineMsg AM)) (Pair (List (Pair AC AE)) (Engine C S B H A AM AC AE))) :=
  let
    -- Create a trigger from the message
    trigger := mkTimestampedTrigger@{
      time := right 0;  -- Dummy time value for now
      trigger := MessageArrived@{msg := msg}
    };
    -- Get the engine's behaviour
    behaviour := Engine.behaviour eng;
    -- Evaluate guards based on strategy
    guardResult := case EngineBehaviour.guards behaviour of {
      | First guards :=
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
      | Any guards := -- What's this actually supposed to do?
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

-- Helper function to evaluate and execute for any engine type
evaluateAndExecuteEng (eng : Eng) (msg : EngineMsg Msg) : Option (Pair (List (EngineMsg Msg)) (Pair (List (Pair Cfg Env)) Eng)) :=
  case eng of {
    | EngIdentityManagement e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngIdentityManagement newEng)))
    }
    | EngDecryption e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngDecryption newEng)))
    }
    | EngEncryption e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngEncryption newEng)))
    }
    | EngCommitment e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngCommitment newEng)))
    }
    | EngVerification e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngVerification newEng)))
    }
    | EngReadsFor e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngReadsFor newEng)))
    }
    | EngSignsFor e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngSignsFor newEng)))
    }
    | EngNaming e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngNaming newEng)))
    }
    | EngLocalKeyValueStorage e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngLocalKeyValueStorage newEng)))
    }
    | EngLogging e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngLogging newEng)))
    }
    | EngWallClock e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngWallClock newEng)))
    }
    | EngLocalTSeries e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngLocalTSeries newEng)))
    }
    | EngRouter e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngRouter newEng)))
    }
    | EngTransportProtocol e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngTransportProtocol newEng)))
    }
    | EngTransportConnection e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngTransportConnection newEng)))
    }
    | EngPubSubTopic e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngPubSubTopic newEng)))
    }
    | EngStorage e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngStorage newEng)))
    }
    | EngMempoolWorker e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngMempoolWorker newEng)))
    }
    | EngExecutor e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngExecutor newEng)))
    }
    | EngShard e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngShard newEng)))
    }
    | EngTicker e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngTicker newEng)))
    }
    | EngTemplate e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngTemplate newEng)))
    }
    | EngTemplateMinimum e := case evaluateAndExecute e msg of {
      | none := none
      | some (mkPair msgs (mkPair cfgEnvPairs newEng)) := some (mkPair msgs (mkPair cfgEnvPairs (EngTemplateMinimum newEng)))
    }
  };

-- Helper function to add a single new engine to the state
addNewEngine (state : NetworkState) (cfg : Cfg) (env : Env) : NetworkState :=
  case mkEng (NetworkState.nextId state) (mkPair cfg env) of {
    | none := state
    | some (mkPair newEng newEngineId) := 
      let
        newId := NetworkState.incrementId state (NetworkState.nextId state);
      in state@NetworkState{
        engines := Map.insert newEngineId newEng (NetworkState.engines state);
        nextId := newId
      }
  };

-- Helper function to update network state based on action effect
updateNetworkState (state : NetworkState) (target : EngineID) (eng : Eng) (msgs : List (EngineMsg Msg)) (cfgEnvPairs : List (Pair Cfg Env)) : NetworkState :=
  let
    -- First update the target engine and messages
    state' := state@NetworkState{
      engines := Map.insert target eng (NetworkState.engines state);
      messages := msgs ++ (NetworkState.messages state)
    };
    -- Then fold over the config/env pairs to create new engines
    finalState := foldl
      (\{s (mkPair cfg env) := addNewEngine s cfg env})
      state'
      cfgEnvPairs
  in finalState;

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
        -- Look up the target engine
        engine := Map.lookup target (NetworkState.engines state);
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

-- Simulate function that runs for a specified number of steps and collects messages
terminating
simulate (selector : MessageSelector) (state : NetworkState) (steps : Nat) : List (EngineMsg Msg) :=
  case steps of {
    | zero := []
    | suc n :=
      let
        -- Apply one step
        next := step selector state;
        -- Get the message if any
        msg := snd next;
        -- Recursively simulate remaining steps
        restMsgs := simulate selector (fst next) n;
      in case msg of {
        | none := restMsgs
        | some m := m :: restMsgs
      }
  };
```
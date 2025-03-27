---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? code "Juvix imports"

    ```juvix
    module arch.system.state.resource_machine.notes.nockma_runnable;
    import prelude open;
    import arch.node.engines.executor_environment open;
    import arch.system.state.resource_machine.notes.nockma open;
    ```

# Nockma Runnable Implementation

This module implements the `Runnable` trait for Nockma, allowing it to be used as an executor in the Anoma system.

## Types

```juvix
-- The program state for Nockma is just the current Noun being evaluated
type NockmaProgramState := mkNockmaProgramState {
  current_noun : Noun;
  storage : Storage Nat Noun;
  gas_limit : Nat;
};
```

## Runnable Instance

```juvix
instance nockmaRunnable : Runnable Nat Nat Noun NockmaProgramState :=
  mkRunnable@{
    -- Execute one step of Nockma evaluation
    executeStep := \{executable state input :=
      let
        -- Convert input key-value pair to a Noun for evaluation
        -- The input value is already a Noun since KVSDatum is Nat
        input_noun := Cell (Atom (fst input)) (Atom (snd input));
        -- Construct the full input noun for Nockma evaluation:
        -- *[a b c] where:
        -- a is the executable program
        -- b is the current program state
        -- c is the input key-value pair
        full_input := Cell (Cell executable (NockmaProgramState.current_noun state)) input_noun;
        -- Run Nockma evaluation with current gas limit
        result := GasState.runGasState (nock (NockmaProgramState.storage state) full_input) (NockmaProgramState.gas_limit state);
      in case result of {
        | error err := error err
        | ok (mkPair result_noun remaining_gas) :=
          -- Parse the result noun which should be of the form (Atom new_state output_requests)
          -- where output_requests is a list encoded as (Atom req1 (Atom req2 (Atom ... (Atom last_req 0))))
          -- A request is either:
          -- - (Atom key value) for write requests
          -- - (Atom key) for read requests
          case result_noun of {
            | Cell (Atom new_state) requests :=
              let
                -- Helper to parse a single request
                parseRequest (req : Noun) : Option (Either Nat (Pair Nat Nat)) :=
                  case req of {
                    | Atom key := some (left key)  -- Read request
                    | Cell (Atom key) (Atom value) := some (right (mkPair key value))  -- Write request
                    | _ := none  -- Invalid request format, ignore it
                  };
                -- Helper to parse the linked list of requests
                terminating
                parseRequests (reqs : Noun) : List (Either Nat (Pair Nat Nat)) :=
                  case reqs of {
                    | Atom zero := nil  -- End of list
                    | Cell (Atom req) rest :=
                      case parseRequest (Atom req) of {
                        | none := parseRequests rest
                        | some parsed := parsed :: parseRequests rest
                      }
                    | _ := nil  -- Invalid request list format, return empty list
                  };
                -- Parse all requests
                parsed_requests := parseRequests requests;
                -- Update program state with new state and remaining gas
                new_state := state@NockmaProgramState{
                  current_noun := Atom new_state;
                  gas_limit := remaining_gas
                };
              in ok (mkPair new_state parsed_requests)
            | _ := error "Invalid result format"
          }
      }
    };

    -- Check if program has halted (out of gas or reached final value)
    halted := \{state :=
      -- Program halts if out of gas or reaches specific state value
      NockmaProgramState.gas_limit state == zero ||
      case NockmaProgramState.current_noun state of {
        | Atom n := n == 1702390132
        | _ := false
      }
    };

    -- Initial program state
    startingState := mkNockmaProgramState@{
      current_noun := Atom zero;  -- Start with empty noun
      storage := externalStorage;  -- Use external storage
      gas_limit := 1000  -- Start with 1000 gas units
    }
  };
```

This implementation:

1. Defines a `NockmaProgramState` type that tracks:
   - The current Noun being evaluated
   - The storage interface for reading/writing Nouns
   - The remaining gas limit

2. Implements `executeStep` to:
   - Convert input key-value pair to a Noun (using direct Atom construction since KVSDatum is Nat)
   - Construct the full input noun for Nockma evaluation using the executable program and current state
   - Run one step of Nockma evaluation
   - Parse the result which should be of the form (Atom new_state output_requests)
   - Parse the output_requests which is a linked list of requests
   - Each request is either:
     - (Atom key) for read requests
     - (Atom key value) for write requests
   - Update program state with new state and remaining gas
   - Return new state and parsed requests

3. Implements `halted` to check if program has run out of gas or is in designated halting state

4. Provides `startingState` with initial values

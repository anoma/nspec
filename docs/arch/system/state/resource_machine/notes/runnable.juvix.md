
---
icon: octicons/container-24
search:
  exclude: false
tags:
  - resource-machine
---

??? code "Juvix imports"

    ```juvix
    module arch.system.state.resource_machine.notes.runnable;
    import prelude open;
    ```

```juvix
trait
type Runnable KVSKey KVSDatum Executable ProgramState :=
  mkRunnable@{
    executeStep : Executable -> ProgramState -> Pair KVSKey KVSDatum -> Result String (Pair ProgramState (List (Either KVSKey (Pair KVSKey KVSDatum))));
    halted : ProgramState -> Bool;
    startingState : ProgramState;
  };
```

`executeStep`:
: Takes the executable code, current program state, and read key-value pair and returns either:
  - Error string on failure
  - New program state and list of either:
    - Left key for read requests
    - Right (key, value) for write requests

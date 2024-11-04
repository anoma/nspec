---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- reads_for
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for;
      import prelude open;
      import arch.node.engines.reads_for_messages open public;
      import arch.node.engines.reads_for_environment open public;
      import arch.node.engines.reads_for_behaviour open public;
      import arch.node.types.engine_behaviour as Anoma;
    ```

# `Reads For` engine behaviour type

<!-- --8<-- [start:reads-for-engine-family] -->
```juvix
ReadsForEngineBehaviour :
  Anoma.EngineBehaviour
    ReadsForLocalState
    ReadsForMailboxState
    ReadsForTimerHandle
    ReadsForMatchableArgument
    ReadsForActionLabel
    ReadsForPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [readsForQueryGuard; submitEvidenceGuard; queryEvidenceGuard];
    action := readsForAction;
    conflictSolver := readsForConflictSolver;
  }
  ;
```
<!-- --8<-- [end:reads-for-engine-family] -->

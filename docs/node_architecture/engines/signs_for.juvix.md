---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- signs_for
- engines
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.signs_for;
      import prelude open;
      import node_architecture.engines.signs_for_overview open public;
      import node_architecture.engines.signs_for_environment open public;
      import node_architecture.engines.signs_for_dynamics open public;
      import node_architecture.types.engine_family as Anoma;
    ```

# `Signs For` engine family type

<!-- --8<-- [start:signs-for-engine-family] -->
```juvix
SignsForEngineFamily :
  Anoma.EngineFamily
    SignsForLocalState
    SignsForMailboxState
    SignsForTimerHandle
    SignsForMatchableArgument
    SignsForActionLabel
    SignsForPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [signsForQueryGuard; submitEvidenceGuard; queryEvidenceGuard];
    action := signsForAction;
    conflictSolver := signsForConflictSolver;
  }
  ;
```
<!-- --8<-- [end:signs-for-engine-family] -->

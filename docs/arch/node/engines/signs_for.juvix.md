---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- signs_for
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for;
      import prelude open;
      import arch.node.engines.signs_for_messages open public;
      import arch.node.engines.signs_for_environment open public;
      import arch.node.engines.signs_for_behaviour open public;
      import arch.node.types.engine_behaviour as Anoma;
    ```

# `Signs For` engine behaviour type

<!-- --8<-- [start:signs-for-engine-family] -->
```juvix
SignsForEngineBehaviour :
  Anoma.EngineBehaviour
    SignsForLocalState
    SignsForMailboxState
    SignsForTimerHandle
    SignsForMatchableArgument
    SignsForActionLabel
    SignsForPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [signsForQueryGuard; submitEvidenceGuard; queryEvidenceGuard];
    action := signsForAction;
    conflictSolver := signsForConflictSolver;
  }
  ;
```
<!-- --8<-- [end:signs-for-engine-family] -->

---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- naming
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.naming;
      import prelude open;
      import arch.node.engines.naming_messages open public;
      import arch.node.engines.naming_environment open public;
      import arch.node.engines.naming_behaviour open public;
      import arch.node.types.engine_behaviour as Anoma;
    ```

# `Naming` engine behaviour type

<!-- --8<-- [start:naming-engine-family] -->
```juvix
NamingEngineBehaviour :
  Anoma.EngineBehaviour
    NamingLocalState
    NamingMailboxState
    NamingTimerHandle
    NamingMatchableArgument
    NamingActionLabel
    NamingPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [resolveNameGuard; submitNameEvidenceGuard; queryNameEvidenceGuard];
    action := namingAction;
    conflictSolver := namingConflictSolver;
  }
  ;
```
<!-- --8<-- [end:naming-engine-family] -->

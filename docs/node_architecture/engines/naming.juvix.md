---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- naming
- engines
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.naming;
      import prelude open;
      import node_architecture.engines.naming_overview open public;
      import node_architecture.engines.naming_environment open public;
      import node_architecture.engines.naming_dynamics open public;
      import node_architecture.types.engine_family as Anoma;
    ```

# `Naming` engine family type

<!-- --8<-- [start:naming-engine-family] -->
```juvix
NamingEngineFamily :
  Anoma.EngineFamily
    NamingLocalState
    NamingMailboxState
    NamingTimerHandle
    NamingMatchableArgument
    NamingActionLabel
    NamingPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [resolveNameGuard; submitNameEvidenceGuard; queryNameEvidenceGuard];
    action := namingAction;
    conflictSolver := namingConflictSolver;
  }
  ;
```
<!-- --8<-- [end:naming-engine-family] -->

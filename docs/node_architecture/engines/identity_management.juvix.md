---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- identity_management
- engines
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.identity_management;
      import prelude open;
      import node_architecture.engines.identity_management_overview open public;
      import node_architecture.engines.identity_management_environment open public;
      import node_architecture.engines.identity_management_dynamics open public;
      import node_architecture.types.engine_family as Anoma;
      import node_architecture.types.anoma_message as Anoma;
    ```

# `Identity Management` engine family type

<!-- --8<-- [start:identity-management-engine-family] -->
```juvix
IdentityManagementEngineFamily :
  Anoma.EngineFamily
    IdentityManagementLocalState
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementMatchableArgument
    IdentityManagementActionLabel
    IdentityManagementPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [generateIdentityGuard; connectIdentityGuard; deleteIdentityGuard];
    action := identityManagementAction;
    conflictSolver := identityManagementConflictSolver;
  }
  ;
```
<!-- --8<-- [end:identity-management-engine-family] -->
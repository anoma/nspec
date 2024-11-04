---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- identity_management
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management;
    import prelude open;
    import arch.node.engines.identity_management_behaviour open public;
    import arch.node.engines.identity_management_environment open public;
    import arch.node.engines.identity_management_messages open public;
    import arch.node.types.anoma_message as Anoma;
    import arch.node.types.engine_behaviour as Anoma;
    ```

# `Identity Management` engine behaviour type

<!-- --8<-- [start:identity-management-engine-family] -->
```juvix
IdentityManagementEngineBehaviour :
  Anoma.EngineBehaviour
    IdentityManagementLocalState
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementMatchableArgument
    IdentityManagementActionLabel
    IdentityManagementPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [generateIdentityGuard; connectIdentityGuard; deleteIdentityGuard];
    action := identityManagementAction;
    conflictSolver := identityManagementConflictSolver;
  }
  ;
```
<!-- --8<-- [end:identity-management-engine-family] -->
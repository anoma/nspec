---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- decryption
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.decryption;
    import prelude open;
    import arch.node.engines.decryption_messages open public;
    import arch.node.engines.decryption_environment open public;
    import arch.node.engines.decryption_behaviour open public;
    import arch.node.types.engine_behaviour as Anoma;
    ```

# `Decryption` engine behaviour type

<!-- --8<-- [start:decryption-engine-family] -->
```juvix
DecryptionEngineBehaviour :
  Anoma.EngineBehaviour
    DecryptionLocalState
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionMatchableArgument
    DecryptionActionLabel
    DecryptionPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [decryptGuard];
    action := decryptionAction;
    conflictSolver := decryptionConflictSolver;
  }
  ;
```
<!-- --8<-- [end:decryption-engine-family] -->

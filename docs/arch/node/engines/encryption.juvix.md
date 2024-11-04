---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- encryption
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.encryption;
      import prelude open;
      import arch.node.types.engine_behaviour as Anoma;
      import arch.node.engines.encryption_behaviour open public;
      import arch.node.engines.encryption_environment open public;
      import arch.node.engines.encryption_messages open public;
    ```

# `Encryption` engine behaviour type

<!-- --8<-- [start:encryption-engine-family] -->
```juvix
EncryptionEngineBehaviour :
  Anoma.EngineBehaviour
    EncryptionLocalState
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionMatchableArgument
    EncryptionActionLabel
    EncryptionPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [encryptGuard; readsForResponseGuard];
    action := encryptionAction;
    conflictSolver := encryptionConflictSolver;
  }
  ;
```
<!-- --8<-- [end:encryption-engine-family] -->
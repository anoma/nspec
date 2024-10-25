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
    module node_architecture.engines.encryption;
      import prelude open;
      import node_architecture.types.engine_family as Anoma;
      import node_architecture.engines.encryption_dynamics open public;
      import node_architecture.engines.encryption_environment open public;
      import node_architecture.engines.encryption_overview open public;
    ```

# `Encryption` engine family type

<!-- --8<-- [start:encryption-engine-family] -->
```juvix
EncryptionEngineFamily :
  Anoma.EngineFamily
    EncryptionLocalState
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionMatchableArgument
    EncryptionActionLabel
    EncryptionPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [encryptGuard; readsForResponseGuard];
    action := encryptionAction;
    conflictSolver := encryptionConflictSolver;
  }
  ;
```
<!-- --8<-- [end:encryption-engine-family] -->
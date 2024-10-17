---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- decryption
- engines
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.decryption;
    import prelude open;
    import node_architecture.engines.decryption_overview open public;
    import node_architecture.engines.decryption_environment open public;
    import node_architecture.engines.decryption_dynamics open public;
    import node_architecture.types.engine_family as Anoma;
    ```

# `Decryption` engine family type

<!-- --8<-- [start:decryption-engine-family] -->
```juvix
DecryptionEngineFamily :
  Anoma.EngineFamily
    DecryptionLocalState
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionMatchableArgument
    DecryptionActionLabel
    DecryptionPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [decryptGuard];
    action := decryptionAction;
    conflictSolver := decryptionConflictSolver;
  }
  ;
```
<!-- --8<-- [end:decryption-engine-family] -->

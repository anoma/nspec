---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- encryption
- engines
---

??? quote "Juvix preamble"

    ```juvix
    module node_architecture.engines.encryption;
    import prelude open;
    import node_architecture.engines.encryption_overview open public;
    import node_architecture.engines.encryption_environment open public;
    import node_architecture.engines.encryption_dynamics open public;
    import node_architecture.types.engine_family as Anoma;
    ```

# Encryption Engine Family Type

```juvix
EncryptionEngineFamily :
  Anoma.EngineFamily
    EncryptionLocalState
    EncryptionMsg
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionMatchableArgument
    EncryptionActionLabel
    EncryptionPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [encryptGuard];
    action := encryptionAction;
    conflictSolver := encryptionConflictSolver;
  };
```
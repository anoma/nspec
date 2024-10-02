---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- decryption
- engines
---

??? quote "Juvix preamble"

    ```juvix
    module node_architecture.engines.decryption;
    import prelude open;
    import node_architecture.engines.decryption_overview open public;
    import node_architecture.engines.decryption_environment open public;
    import node_architecture.engines.decryption_dynamics open public;
    import node_architecture.types.engine_family as Anoma;
    ```

# Decryption Engine Family Type

```juvix
DecryptionEngineFamily :
  Anoma.EngineFamily
    DecryptionLocalState
    DecryptionMsg
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionMatchableArgument
    DecryptionActionLabel
    DecryptionPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [decryptGuard];
    action := decryptionAction;
    conflictSolver := decryptionConflictSolver;
  };
```
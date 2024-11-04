---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- commitment
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.commitment;
      import prelude open;
      import arch.node.engines.commitment_messages open public;
      import arch.node.engines.commitment_environment open public;
      import arch.node.engines.commitment_behaviour open public;
      import arch.node.types.engine_behaviour as Anoma;
    ```

# `Commitment` engine behaviour type

<!-- --8<-- [start:commitment-engine-family] -->
```juvix
CommitmentEngineBehaviour :
  Anoma.EngineBehaviour
    CommitmentLocalState
    CommitmentMailboxState
    CommitmentTimerHandle
    CommitmentMatchableArgument
    CommitmentActionLabel
    CommitmentPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [commitGuard];
    action := commitmentAction;
    conflictSolver := commitmentConflictSolver;
  };
```
<!-- --8<-- [end:commitment-engine-family] -->
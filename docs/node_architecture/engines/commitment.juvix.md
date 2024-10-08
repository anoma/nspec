---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- commitment
- engines
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.commitment;
      import prelude open;
      import node_architecture.engines.commitment_overview open public;
      import node_architecture.engines.commitment_environment open public;
      import node_architecture.engines.commitment_dynamics open public;
      import node_architecture.types.engine_family as Anoma;
    ```

# `Commitment` engine family type

<!-- --8<-- [start:commitment-engine-family] -->
```juvix
CommitmentEngineFamily :
  Anoma.EngineFamily
    CommitmentLocalState
    CommitmentMailboxState
    CommitmentTimerHandle
    CommitmentMatchableArgument
    CommitmentActionLabel
    CommitmentPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [commitGuard];
    action := commitmentAction;
    conflictSolver := commitmentConflictSolver;
  };
```
<!-- --8<-- [end:commitment-engine-family] -->
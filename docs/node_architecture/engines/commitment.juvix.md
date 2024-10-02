---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- commitment
- engines
---

??? quote "Juvix preamble"

    ```juvix
    module node_architecture.engines.commitment;
    import prelude open;
    import node_architecture.engines.commitment_overview open public;
    import node_architecture.engines.commitment_environment open public;
    import node_architecture.engines.commitment_dynamics open public;
    import node_architecture.types.engine_family as Anoma;
    ```

# Commitment Engine Family Type

```juvix
CommitmentEngineFamily :
  Anoma.EngineFamily
    CommitmentLocalState
    CommitmentMsg
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
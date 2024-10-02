---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- reads_for
- engines
---

??? quote "Juvix preamble"

    ```juvix
    module node_architecture.engines.reads_for;
    import prelude open;
    import node_architecture.engines.reads_for_overview open public;
    import node_architecture.engines.reads_for_environment open public;
    import node_architecture.engines.reads_for_dynamics open public;
    import node_architecture.types.engine_family as Anoma;
    ```
    
# Reads For Engine Family Type

```juvix
ReadsForEngineFamily :
  Anoma.EngineFamily
    ReadsForLocalState
    ReadsForMsg
    ReadsForMailboxState
    ReadsForTimerHandle
    ReadsForMatchableArgument
    ReadsForActionLabel
    ReadsForPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [readsForQueryGuard; submitEvidenceGuard; queryEvidenceGuard];
    action := readsForAction;
    conflictSolver := readsForConflictSolver;
  };
```
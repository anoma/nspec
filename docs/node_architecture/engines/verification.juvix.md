---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- verification
- engines
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.verification;
      import prelude open;
      import node_architecture.engines.verification_overview open public;
      import node_architecture.engines.verification_environment open public;
      import node_architecture.engines.verification_dynamics open public;
      import node_architecture.types.engine_family as Anoma;
    ```

# `Verification` engine family type

<!-- --8<-- [start:verification-engine-family] -->
```juvix
VerificationEngineFamily :
  Anoma.EngineFamily
    VerificationLocalState
    VerificationMsg
    VerificationMailboxState
    VerificationTimerHandle
    VerificationMatchableArgument
    VerificationActionLabel
    VerificationPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [verifyGuard];
    action := verificationAction;
    conflictSolver := verificationConflictSolver;
  }
  ;
```
<!-- --8<-- [end:verification-engine-family] -->
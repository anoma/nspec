---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- verification
- engines
---

??? quote "Juvix preamble"

    ```juvix
    module node_architecture.engines.verification;
    import prelude open;
    import node_architecture.engines.verification_overview open public;
    import node_architecture.engines.verification_environment open public;
    import node_architecture.engines.verification_dynamics open public;
    import node_architecture.types.engine_family as Anoma;
    ```

# Verification Engine Family Type

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
  };
```
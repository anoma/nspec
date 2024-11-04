---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- verification
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.verification;
      import prelude open;
      import arch.node.engines.verification_messages open public;
      import arch.node.engines.verification_environment open public;
      import arch.node.engines.verification_behaviour open public;
      import arch.node.types.engine_behaviour as Anoma;
    ```

# `Verification` engine behaviour type

<!-- --8<-- [start:verification-engine-family] -->
```juvix
VerificationEngineBehaviour :
  Anoma.EngineBehaviour
    VerificationLocalState
    VerificationMailboxState
    VerificationTimerHandle
    VerificationMatchableArgument
    VerificationActionLabel
    VerificationPrecomputation
  := Anoma.mkEngineBehaviour@{
    guards := [verifyGuard; signsForResponseGuard];
    action := verificationAction;
    conflictSolver := verificationConflictSolver;
  }
  ;
```
<!-- --8<-- [end:verification-engine-family] -->
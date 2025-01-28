---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- verification-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.verification;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.verification_config open public;
    import arch.node.engines.verification_messages open public;
    import arch.node.engines.verification_environment open public;
    import arch.node.engines.verification_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open verification_config_example;
    open verification_environment_example;
    ```

# Verification Engine

The Verification Engine is responsible for verifying commitments (signatures) made by
external identities. It automatically uses "signs_for" relationship information from
the [[SignsFor Engine]] along with caller preference information to determine how
to verify a commitment.

## Purpose

The Verification Engine verifies commitments (signatures) made by external identities.
It can use "signs_for" relationship information and caller preferences to determine how
to verify a commitment. This engine is designed to be stateless, allowing for efficient
implementation by the runtime.

## Engine components

- [[Verification Messages]]
- [[Verification Configuration]]
- [[Verification Environment]]
- [[Verification Behaviour]]

## Type

<!-- --8<-- [start:VerificationEngine] -->
```juvix
VerificationEngine : Type :=
  Engine
    VerificationCfg
    VerificationLocalState
    VerificationMailboxState
    VerificationTimerHandle
    VerificationActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:VerificationEngine] -->

### Example of a verification engine

<!-- --8<-- [start:exampleVerificationEngine] -->
```juvix
exampleVerificationEngine : VerificationEngine :=
  mkEngine@{
    cfg := verificationCfg;
    env := verificationEnv;
    behaviour := verificationBehaviour;
  };
```
<!-- --8<-- [end:exampleVerificationEngine] -->

where `verificationCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/verification_config.juvix.md:verificationCfg"

`verificationEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/verification_environment.juvix.md:verificationEnv"

and `verificationBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/verification_behaviour.juvix.md:verificationBehaviour"

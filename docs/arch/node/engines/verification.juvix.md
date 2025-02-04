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

The Verification Engine provides signature verification services within Anoma. It can check
cryptographic signatures/commitments (a `Commitment`) against data (a `Signable`) in two modes: direct
verification against a specified identity, or verification that takes into account "signs_for"
relationships through integration with a [[SignsFor Engine]] (specified via
`signsForEngineAddress` in its configuration) which allows some identities to sign on
behalf of other identities. One may compare the verification service to how a notary might verify not
just a signature, but also check if the signer had proper authority to sign on behalf of another party.

When users submit a verification request (via a `MsgVerificationRequest` message), they provide the
data, the commitment/signature to verify, the supposed external identity that made the commitment,
and whether to use signs-for relationships (via the `useSignsFor` flag). If signs-for checking is
disabled, the engine directly verifies the signature using the configured verifier. If signs-for
checking is enabled, the engine first queries the SignsFor Engine for evidence of signing
relationships, then uses this additional context during verification. The engine returns a boolean
result (via a `MsgVerificationReply` message) indicating whether the signature is valid.

The verification process is atomic - each request either succeeds with a clear yes/no answer or fails
with an error message. The engine's state only keeps track of pending requests when signs-for relationships need to be checked.
Requests are added to a queue associated with the request, and this queue is cleared once information
is provided by the SignsFor Engine.

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

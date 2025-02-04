---
icon: octicons/project-template-24
search:
  exclude: false
categories:
- engine
tags:
- encryption-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.encryption;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.encryption_messages open public;
    import arch.node.engines.encryption_environment open public;
    import arch.node.engines.encryption_behaviour open public;

    import arch.node.engines.encryption_config open public;
    import arch.node.engines.encryption_messages open public;
    import arch.node.engines.encryption_environment open public;
    import arch.node.engines.encryption_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open encryption_config_example;
    open encryption_environment_example;
    ```

# Encryption Engine

The Encryption Engine provides encryption services within Anoma, allowing data to be securely
encrypted for specific identities while supporting flexible encryption policies through integration
with reads-for relationships. One may think of it as a smart mail service that can seal messages so that
only intended recipients can read them, with the additional ability to consider pre-approved sharing
relationships when sealing the message.

When users request encryption (via a `MsgEncryptionRequest` message), they provide the data to encrypt
(a `Plaintext`), the target identity (an `ExternalIdentity`), and whether to consider reads-for
relationships (`useReadsFor`). The engine has two main operating modes:

Direct encryption (`useReadsFor: false`)

: The engine immediately encrypts the data for the
specified identity and returns the encrypted result (via s `MsgEncryptionReply` containing a
`Ciphertext`).

ReadsFor-aware encryption (`useReadsFor: true`)

: The engine first queries a [[ReadsFor Engine]] to
check for any relevant reads-for relationships, then encrypts the data in a way that respects these
relationships. This mode enables scenarios where data should be accessible not just to the direct
recipient, but also to other identities with approved access rights.

??? info "On spawning"

    The engine is spawned by the system
    when encryption services are needed and operates statelessly
    except when handling reads-for queries.
    For reads-for cases,
    it maintains a temporary queue of pending encryption requests
    while waiting for relationship evidence.

## Engine components

- [[Encryption Messages]]
- [[Encryption Configuration]]
- [[Encryption Environment]]
- [[Encryption Behaviour]]

## Type

<!-- --8<-- [start:EncryptionEngine] -->
```juvix
EncryptionEngine : Type :=
  Engine
    EncryptionCfg
    EncryptionLocalState
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:EncryptionEngine] -->

### Example of a encryption engine

<!-- --8<-- [start:exampleEncryptionEngine] -->
```juvix
exampleEncryptionEngine : EncryptionEngine :=
  mkEngine@{
    cfg := encryptionCfg;
    env := encryptionEnv;
    behaviour := encryptionBehaviour;
  };
```
<!-- --8<-- [end:exampleEncryptionEngine] -->

where `encryptionCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_config.juvix.md:encryptionCfg"

`encryptionEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_environment.juvix.md:encryptionEnv"

and `encryptionBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_behaviour.juvix.md:encryptionBehaviour"

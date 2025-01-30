---
icon: octicons/gear-16
search:
  exclude: false
tags:
- node-architecture
- identity
- engine
- decryption
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.decryption;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.decryption_config open public;
    import arch.node.engines.decryption_messages open public;
    import arch.node.engines.decryption_environment open public;
    import arch.node.engines.decryption_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open decryption_config_example;
    open decryption_environment_example;
    ```

# Decryption Engine

The Decryption Engine serves as a secure decryption service for a
specific identity within Anoma. It functions like a secure lockbox
that can decrypt messages (ciphertext to plaintext) intended for its
associated identity, while keeping the decryption keys secure and
unexposed. This enables secure communication where only the intended
recipient can read encrypted messages.

When users submit encrypted data to the engine
(via a `MsgDecryptionRequest` message), it validates their
authorisation and returns the decrypted content
(via a `MsgDecryptionReply` message) if the decryption is
successful.

In Anoma, Decryption Engines are only spawned by
[[Identity Management Engine|Identity Management Engines]] during identity
creation or connection. Only users with the engine reference can request
decryption. This ensures that encrypted data can only be decrypted by
authorised parties while maintaining the security of the private
decryption keys.

## Engine components

- [[Decryption Messages]]
- [[Decryption Configuration]]
- [[Decryption Environment]]
- [[Decryption Behaviour]]

## The type for a decryption engine

<!-- --8<-- [start:DecryptionEngine] -->
```juvix
DecryptionEngine : Type :=
  Engine
    DecryptionCfg
    DecryptionLocalState
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:DecryptionEngine] -->

### Example of a decryption engine


<!-- --8<-- [start:exampleDecryptionEngine] -->
```juvix
exampleDecryptionEngine : DecryptionEngine :=
  mkEngine@{
    cfg := decryptionCfg;
    env := decryptionEnv;
    behaviour := decryptionBehaviour;
  };
```
<!-- --8<-- [end:exampleDecryptionEngine] -->

where [[Decryption Configuration#decryptionCfg|`decryptionCfg`]] is defined as follows:

--8<-- "./docs/arch/node/engines/decryption_config.juvix.md:decryptionCfg"

[[Decryption Environment#decryptionEnv|`decryptionEnv`]] is defined as follows:

--8<-- "./docs/arch/node/engines/decryption_environment.juvix.md:decryptionEnv"

and [[Decryption Behaviour#decryptionBehaviour|`decryptionBehaviour`]] is defined as follows:

--8<-- "./docs/arch/node/engines/decryption_behaviour.juvix.md:decryptionBehaviour"

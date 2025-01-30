---
icon: octicons/container-24
search:
  exclude: false
tags:
- node-architecture
- identity
- engine
- decryption
- configuration
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.decryption_config;

    import prelude open;
    import arch.node.engines.decryption_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.system.identity.identity open using {Decryptor; mkDecryptor};
    import arch.node.types.identities open;
    ```

# Decryption Configuration

## Overview

The decryption engine configuration contains static information for decryption engine instances.

## The Decryption Configuration

The configuration of a Decryption Engine instance includes the identity's
decryption capabilities.

### `DecryptionCfg`

<!-- --8<-- [start:DecryptionCfg] -->
```juvix
type DecryptionCfg := mkDecryptionCfg@{
  decryptor : Decryptor Backend Plaintext Ciphertext;
  backend : Backend;
};
```
<!-- --8<-- [end:DecryptionCfg] -->

???+ quote "Arguments"

    `decryptor`:
    : The decryptor for the decrypting.

    `backend`:
    : The backend to use for decryption.

#### Instantiation

<!-- --8<-- [start:decryptionCfg] -->
```juvix extract-module-statements
module decryption_config_example;

  decryptionCfg : EngineCfg DecryptionCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "decryption";
      cfg := mkDecryptionCfg@{
        decryptor := mkDecryptor@{
          decrypt := \{_ x := some x};
        };
        backend := BackendLocalMemory;
      };
    }
  ;
end;
```
<!-- --8<-- [end:decryptionCfg] -->

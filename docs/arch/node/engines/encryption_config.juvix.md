---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- encryption-engine
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.encryption_config;

    import prelude open;
    import arch.node.engines.encryption_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
    ```

# Encryption Configuration

## Overview

The Encryption engine configuration contains static information for Encryption engine instances.

## The Encryption Configuration

The configuration of an `Encryption` Engine instance includes the identity's
encryption capabilities, the address of an associated `ReadsFor` engine, and a
specific backend.

### `EncryptionCfg`

<!-- --8<-- [start:EncryptionCfg] -->
```juvix
type EncryptionCfg := mkEncryptionCfg {
  encryptor : Set ReadsForEvidence -> ExternalIdentity -> Encryptor ByteString Backend Plaintext Ciphertext;
  backend : Backend;
  readsForEngineAddress : EngineID;
}
```
<!-- --8<-- [end:EncryptionCfg] -->

???+ quote "Arguments"

    `encryptor`:
    : Function to generate encryptor for a set of evidence and an identity.

    `backend`:
    : The backend to use for encryption.

    `readsForEngineAddress`:
    : The address of the associated ReadFor engine.

#### Instantiation

<!-- --8<-- [start:encryptionCfg] -->
```juvix extract-module-statements
module encryption_config_example;

  encryptionCfg : EngineCfg EncryptionCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "encryption";
      cfg := mkEncryptionCfg@{
        encryptor := \{_ _ := mkEncryptor@{
          encrypt := \{_ x := x};
          encryptorHash := mkHASH@{
            ordKey := mkOrdkey@{
                compare := Ord.cmp
            };
            hash := \{x := "0x1234abcd"};
          };
        }};
        backend := BackendLocalMemory;
        readsForEngineAddress := mkPair none "Blah";
      };
    }
  ;
end;
```
<!-- --8<-- [end:encryptionCfg] -->

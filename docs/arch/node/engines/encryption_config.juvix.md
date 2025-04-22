---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - encryption
  - configuration
---

??? code "Juvix imports"

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

## The Encryption Local Configuration

The configuration of an `Encryption` Engine instance includes the identity's
encryption capabilities, the address of an associated `ReadsFor` engine, and a
specific backend.

### `EncryptionLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:EncryptionLocalCfg] -->
```juvix
type EncryptionLocalCfg := mk {
  encryptor : Set ReadsForEvidence -> ExternalIdentity -> Encryptor ByteString Backend Plaintext Ciphertext;
  backend : Backend;
  readsForEngineAddress : EngineID;
}
```
<!-- --8<-- [end:EncryptionLocalCfg] -->

???+ code "Arguments"

    `encryptor`:
    : Function to generate encryptor for a set of evidence and an identity.

    `backend`:
    : The backend to use for encryption.

    `readsForEngineAddress`:
    : The address of the associated ReadFor engine.

## The Encryption Configuration

### `EncryptionCfg`

<!-- --8<-- [start:EncryptionCfg] -->
```juvix
EncryptionCfg : Type :=
  EngineCfg
    EncryptionLocalCfg;
```
<!-- --8<-- [end:EncryptionCfg] -->

#### Instantiation

<!-- --8<-- [start:encryptionCfg] -->
```juvix extract-module-statements
module encryption_config_example;

  encryptionCfg : EncryptionCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "encryption";
      cfg := EncryptionLocalCfg.mk@{
        encryptor := \{_ _ := Encryptor.mkEncryptor@{
          encrypt := \{_ x := x};
          encryptorHash := HASH.mkHASH@{
            ordKey := OrdKey.mkOrdKey@{
                compare := Ord.compare
            };
            hash := \{x := "0x1234abcd"};
          };
        }};
        backend := Backend.LocalMemory;
        readsForEngineAddress := mkPair none "Blah";
      };
    }
  ;
end;
```
<!-- --8<-- [end:encryptionCfg] -->

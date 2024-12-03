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

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.encryption_config;

    import prelude open;
    import arch.node.engines.encryption_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Encryption Configuration

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Encryption Configuration

### `EncryptionCfg`

<!-- --8<-- [start:EncryptionCfg] -->
```juvix
type EncryptionCfg := mkEncryptionCfg
```
<!-- --8<-- [end:EncryptionCfg] -->

#### Instantiation

<!-- --8<-- [start:encryptionCfg] -->
```juvix extract-module-statements
module encryption_config_example;

  encryptionCfg : EngineCfg EncryptionCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "encryption";
      cfg := mkEncryptionCfg
    }
  ;
end;
```
<!-- --8<-- [end:encryptionCfg] -->

---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- decryption-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.decryption_config;

    import prelude open;
    import arch.node.engines.decryption_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Decryption Configuration

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Decryption Configuration

### `DecryptionCfg`

<!-- --8<-- [start:DecryptionCfg] -->
```juvix
type DecryptionCfg :=
  mkDecryptionCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:DecryptionCfg] -->

#### Instantiation

<!-- --8<-- [start:decryptionCfg] -->
```juvix extract-module-statements
module decryption_config_example;

  decryptionCfg : EngineCfg DecryptionCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "decryption";
      cfg := mkDecryptionCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:decryptionCfg] -->

---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- verification-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.verification_config;

    import prelude open;
    import arch.node.engines.verification_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Verification Configuration

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Verification Configuration

### `VerificationCfg`

<!-- --8<-- [start:VerificationCfg] -->
```juvix
type VerificationCfg :=
  mkVerificationCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:VerificationCfg] -->

#### Instantiation

<!-- --8<-- [start:verificationCfg] -->
```juvix extract-module-statements
module verification_config_example;

  verificationCfg : EngineCfg VerificationCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "verification";
      cfg := mkVerificationCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:verificationCfg] -->

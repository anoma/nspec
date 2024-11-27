---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- commitment-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.commitment_config;

    import prelude open;
    import arch.node.engines.commitment_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Commitment Configuration

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Commitment Configuration

### `CommitmentCfg`

<!-- --8<-- [start:CommitmentCfg] -->
```juvix
type CommitmentCfg :=
  mkCommitmentCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:CommitmentCfg] -->

#### Instantiation

<!-- --8<-- [start:commitmentCfg] -->
```juvix extract-module-statements
module commitment_config_example;

  commitmentCfg : EngineCfg CommitmentCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "commitment";
      cfg := mkCommitmentCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:commitmentCfg] -->

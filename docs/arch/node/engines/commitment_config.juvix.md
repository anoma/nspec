---
icon: octicons/container-24
search:
  exclude: false
tags:
- node-architecture
- identity-subsystem
- engine
- commitment
- configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.commitment_config;

    import prelude open;
    import arch.node.engines.commitment_messages open;
    import arch.system.identity.identity open using {Signer; mkSigner};
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Commitment Configuration

## Overview

The commitment engine configuration contains static information for commitment engine instances.

## The Commitment Configuration

The configuration of a Commitment Engine instance includes the identity's signing capabilities.

### `CommitmentCfg`

<!-- --8<-- [start:CommitmentCfg] -->
```juvix
type CommitmentCfg := mkCommitmentCfg@{
  signer : Signer Backend Signable Commitment;
  backend : Backend;
};
```
<!-- --8<-- [end:CommitmentCfg] -->

???+ code "Arguments"

    `signer`:
    : The signer for the identity.

    `backend`:
    : The backend to use for signing.

#### Instantiation

<!-- --8<-- [start:commitmentCfg] -->
```juvix extract-module-statements
module commitment_config_example;

  commitmentCfg : EngineCfg CommitmentCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "commitment";
      cfg := mkCommitmentCfg@{
        signer := mkSigner@{
          sign := \{_ x := Ed25519Signature "0xabcd1234"};
        };
        backend := BackendLocalMemory;
      };
    }
  ;
end;
```
<!-- --8<-- [end:commitmentCfg] -->

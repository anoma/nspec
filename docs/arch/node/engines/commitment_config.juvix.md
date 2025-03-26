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

The commitment engine configuration contains static information for commitment engine instances, namely the signer and the backend.

## The Commitment Local Configuration

### `CommitmentLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:CommitmentLocalCfg] -->
```juvix
type CommitmentLocalCfg := mkCommitmentLocalCfg@{
  signer : Signer Backend Signable Commitment;
  backend : Backend;
};
```
<!-- --8<-- [end:CommitmentLocalCfg] -->

???+ code "Arguments"

    `signer`:
    : The signer for the identity.

    `backend`:
    : The backend to use for signing.

## The Commitment Configuration

### `CommitmentCfg`

<!-- --8<-- [start:CommitmentCfg] -->
```juvix
CommitmentCfg : Type :=
  EngineCfg
    CommitmentLocalCfg;
```
<!-- --8<-- [end:CommitmentCfg] -->

#### Instantiation

<!-- --8<-- [start:commitmentCfg] -->
```juvix extract-module-statements
module commitment_config_example;

  commitmentCfg : CommitmentCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "commitment";
      cfg := mkCommitmentLocalCfg@{
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

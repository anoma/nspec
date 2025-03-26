---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - identity-management
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management_config;

    import prelude open;
    import arch.node.engines.identity_management_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Identity Management Configuration

## Overview

The Identity Management engine configuration contains static information for Identity Management engine instances.

## The Identity Management Local Configuration

### `IdentityManagementLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:IdentityManagementLocalCfg] -->
```juvix
type IdentityManagementLocalCfg := mkIdentityManagementLocalCfg;
```
<!-- --8<-- [end:IdentityManagementLocalCfg] -->

## The Identity Management Configuration

### `IdentityManagementCfg`

<!-- --8<-- [start:IdentityManagementCfg] -->
```juvix
IdentityManagementCfg : Type :=
  EngineCfg
    IdentityManagementLocalCfg;
```
<!-- --8<-- [end:IdentityManagementCfg] -->

#### Instantiation

<!-- --8<-- [start:identityManagementCfg] -->
```juvix extract-module-statements
module identity_management_config_example;

  identityManagementCfg : IdentityManagementCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "identity management";
      cfg := mkIdentityManagementLocalCfg;
    }
  ;
end;
```
<!-- --8<-- [end:identityManagementCfg] -->

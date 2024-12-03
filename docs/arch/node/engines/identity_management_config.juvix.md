---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- identity-management-engine
- engine-environment
---

??? note "Juvix imports"

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

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Identity Management Configuration

### `IdentityManagementCfg`

<!-- --8<-- [start:IdentityManagementCfg] -->
```juvix
type IdentityManagementCfg := mkIdentityManagementCfg
```
<!-- --8<-- [end:IdentityManagementCfg] -->

#### Instantiation

<!-- --8<-- [start:identityManagementCfg] -->
```juvix extract-module-statements
module identity_management_config_example;

  identityManagementCfg : EngineCfg IdentityManagementCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "identity management";
      cfg := mkIdentityManagementCfg
    }
  ;
end;
```
<!-- --8<-- [end:identityManagementCfg] -->

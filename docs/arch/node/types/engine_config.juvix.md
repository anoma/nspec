---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Engine
- Config
- Configuration
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.engine_config;

    import arch.node.types.basics open public;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Engine configuration

## Engine configuration type

The engine configuration contains the following static information for engine instances:

- A global reference, `name`, for the engine instance.
- The local `NodeID`.
- Engine-specific configuration.

This is defined in the `EngineCfg` type,
which is parametrized by:

- `C`: represents the engine-specific configuration, which corresponds to the `Cfg` type.

```juvix
type EngineCfg (C : Type) :=
  mkEngineCfg@{
    node : NodeID;
    name : EngineName;
    cfg : C;
  };
```

### `getEngineIDFromEngineCfg`

- Get the local `EngineID` from an `EngineCfg`:

```juvix
getEngineIDFromEngineCfg {C} (cfg : EngineCfg C) : EngineID :=
  mkPair (some (EngineCfg.node cfg)) (EngineCfg.name cfg);
```

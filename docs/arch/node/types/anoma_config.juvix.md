---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_config;

    -- import arch.node.engines.ticker_config open;
    ```

# Anoma Engine Configuration

An _Anoma_ engine configuration contains static, read-only configuration for an engine.
See [[Engine Configuration]] for more information.

Below is the definition of the type `Config`,
which represents an Anoma engine configuration.
This means, an Anoma engine instance would have a configuration of type `Config`.

For example, a configuration for an engine instance
of the engine `TickerEngine` is of type `TickerCfg`.

<!-- --8<-- [start:anoma-config-type] -->
```juvix
type Cfg :=
  | CfgTicker -- TickerCfg
```
<!-- --8<-- [end:anoma-config-type] -->

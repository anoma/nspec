---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- ticker-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.ticker_config;

    import prelude open;
    import arch.node.engines.ticker_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Ticker Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## The Ticker Local Configuration

### `TickerLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:TickerLocalCfg] -->
```juvix
type TickerLocalCfg :=
  mkTickerLocalCfg;
```
<!-- --8<-- [end:TickerLocalCfg] -->

## The Ticker Configuration

### `TickerCfg`

<!-- --8<-- [start:TickerCfg] -->
```juvix
TickerCfg : Type :=
  EngineCfg
    TickerLocalCfg;
```
<!-- --8<-- [end:TickerCfg] -->

#### Instantiation

<!-- --8<-- [start:tickerCfg] -->
```juvix extract-module-statements
module ticker_config_example;

  tickerCfg : TickerCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "ticker";
      cfg := mkTickerLocalCfg;
    }
  ;
end;
```
<!-- --8<-- [end:tickerCfg] -->

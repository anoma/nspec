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

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Ticker Configuration

### `TickerCfg`

<!-- --8<-- [start:TickerCfg] -->
```juvix
type TickerCfg :=
  mkTickerCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:TickerCfg] -->

#### Instantiation

<!-- --8<-- [start:tickerCfg] -->
```juvix extract-module-statements
module ticker_config_example;

  tickerCfg : EngineCfg TickerCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "ticker";
      cfg := mkTickerCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:tickerCfg] -->

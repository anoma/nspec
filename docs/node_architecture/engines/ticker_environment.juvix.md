---
icon: octicons/container-24
search:
  exclude: false
---

# Ticker Environment

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.ticker_environment;

    import prelude open;
    import node_architecture.engines.ticker_overview open;
    import node_architecture.types.engine_environment open;
    ```

## Overview

The sole data item of the ticker environment that deserves mention is
the counter;
we do not need timers, or mailbox state.

## Mailbox states

```juvix
syntax alias TickerMailboxState := Unit;
```

The [[Ticker engine family|ticker]] does not rely on mailbox-relative state.

## Local state

```juvix
type TickerLocalState : Type := mkTickerLocalState {
  counter : Nat
};
```

The local state of [[Ticker engine family|tickers]]
consists of a single counter,
storing a non-negative integer value.

## Timer Handle

```juvix
syntax alias TickerTimerHandle := Unit;
```

The [[Ticker engine family|ticker]] does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.


## Environment summary

```juvix
TickerEnvironment : Type :=
  EngineEnvironment
    TickerLocalState
    TickerMsg
    TickerMailboxState
    TickerTimerHandle;
```

## Example of a `Ticker` environment

```juvix extract-module-statements
module ticker_environment_example;

tickerEnvironmentExample : TickerEnvironment :=
    mkEngineEnvironment@ {
      name := Left "ticker"; -- Name
      localState := mkTickerLocalState@{
        counter := 0
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```


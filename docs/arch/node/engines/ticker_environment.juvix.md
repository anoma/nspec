---
icon: octicons/container-24
search:
  exclude: false
---

# Ticker Environment

??? note "Juvix preamble"

    ```juvix
    module arch.node.engines.ticker_environment;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.engines.ticker_messages open;
    import arch.node.types.engine_environment open;
    ```

## Overview

The sole data item of the ticker environment that deserves mention is
the counter;
we do not need timers, or mailbox state.

## Mailbox states

```juvix
syntax alias TickerMailboxState := Unit;
```

## Local state

```juvix
type TickerLocalState : Type := mkTickerLocalState {
  counter : Nat
};
```

## Timer Handle

```juvix
syntax alias TickerTimerHandle := Unit;
```

The [[Ticker Engine Overview|ticker]] does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
TickerEnvironment : Type := EngineEnvironment TickerLocalState TickerMailboxState TickerTimerHandle;
```

## Example of a `Ticker` environment

```juvix extract-module-statements
module ticker_environment_example;

tickerEnvironmentExample : TickerEnvironment :=
    mkEngineEnvironment@{
      name := "ticker";
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
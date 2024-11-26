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

# Ticker Environment

??? quote "Juvix preamble"

    ```juvix
    module arch.node.engines.ticker_environment;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.engines.ticker_messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
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
type TickerLocalState := mkTickerLocalState@{
  counter : Nat
};
```

???+ quote "Arguments"

    `counter`:
    : The counter value.

## Timer Handle

```juvix
syntax alias TickerTimerHandle := Unit;
```

The [[Ticker Engine Overview|ticker]] does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

## Timestamped Trigger

<!-- --8<-- [start:TemplateTimestampedTrigger] -->
```juvix
TickerTimestampedTrigger : Type :=
  TimestampedTrigger
    TickerTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateTimestampedTrigger] -->

## The Ticker Environment

### `TickerEnv`

```juvix
TickerEnv : Type :=
  EngineEnv
    TickerLocalState
    TickerMailboxState
    TickerTimerHandle
    Anoma.Msg;
```

#### Instantiation

<!-- --8<-- [roTickerEnvironment] -->
```juvix extract-module-statements
module ticker_environment_example;

tickerEnv : TickerEnv :=
  mkEngineEnv@{
    localState := mkTickerLocalState@{
      counter := 0
    };
    mailboxCluster := Map.empty;
    acquaintances := Set.empty;
    timers := []
  };
end;
```
<!-- --8<-- [TickerEnvironment] -->

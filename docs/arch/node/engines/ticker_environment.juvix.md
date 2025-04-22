---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - example
  - engine
  - ticker
  - environment
---

# Ticker Environment

??? code "Juvix imports"

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
type TickerLocalState := mk@{
  counter : Nat
};
```

???+ code "Arguments"

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

<!-- --8<-- [start:TickerEnv] -->
```juvix
TickerEnv : Type :=
  EngineEnv
    TickerLocalState
    TickerMailboxState
    TickerTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TickerEnv] -->

#### Instantiation

<!-- --8<-- [start:tickerEnv] -->
```juvix extract-module-statements
module ticker_environment_example;

tickerEnv : TickerEnv :=
  EngineEnv.mk@{
    localState := TickerLocalState.mk@{
      counter := 0
    };
    mailboxCluster := Map.empty;
    acquaintances := Set.Set.empty;
    timers := []
  };
end;
```
<!-- --8<-- [end:exampleTickerEnvironment] -->

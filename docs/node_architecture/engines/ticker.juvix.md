---
icon: octicons/gear-16
search:
  exclude: false
tags:
- engines
- conventions
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.ticker;

    import node_architecture.engines.ticker_messages open public;
    import node_architecture.engines.ticker_environment open public;
    import node_architecture.engines.ticker_behaviour open public;

    import prelude open;
    import node_architecture.types.engine open;
    ```

# Ticker Engine

The Ticker engine provides a simple counter functionality, allowing
clients to increment a counter and retrieve its current value.

## Purpose

A ticker engine maintains a counter in its local state. It increases the counter
when it receives an `Increment` message and provides the updated result upon
receiving a `Count` message. The initial state initializes the counter.

## Components

- [[Ticker Messages]]
- [[Ticker Environment]]
- [[Ticker Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

### `TickerBehaviour`

<!-- --8<-- [start:TickerBehaviour] -->
```juvix
TickerBehaviour :
  EngineBehaviour
    TickerLocalState
    TickerMailboxState
    TickerTimerHandle
    TickerMatchableArgument
    TickerActionLabel
    TickerPrecomputation
  := mkEngineBehaviour@{
    guards := [incrementGuard ; countGuard];
    action := tickerAction;
    conflictSolver := tickerConflictSolver;
  }
  ;
```
<!-- --8<-- [end:TickerBehaviour] -->

### `TickerEngine`

<!-- --8<-- [start:TickerEngine] -->
```TODO juvix
TickerEngine : Engine
  TickerLocalState
  TickerMailboxState
  TickerTimerHandle
  TickerMatchableArgument
  TickerActionLabel
  TickerPrecomputation := mkEngine@{
    name := "ticker";
    behaviour := TickerBehaviour;
    initEnv := mkEngineEnvironment@{
      name := "ticker";
      localState := Unit;
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := [];
  };
};
```
<!-- --8<-- [end:TickerEngine] -->

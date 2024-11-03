---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
- node
tags:
- ticker-engine
- engine-definition
---

??? quote "Juvix preamble"

    ```juvix
    module arch.node.engines.ticker;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.ticker_messages open public;
    import arch.node.engines.ticker_environment open public;
    import arch.node.engines.ticker_behaviour open public;
    open ticker_environment_example;
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

<!-- --8<-- [start:TickerEngine] -->
```juvix
TickerEngine : Type := Engine
  TickerLocalState
  TickerMailboxState
  TickerTimerHandle
  TickerMatchableArgument
  TickerActionLabel
  TickerPrecomputation;
```
<!-- --8<-- [end:TickerEngine] -->

### Example of a ticker engine

<!-- --8<-- [start:example-ticker-engine] -->
```juvix extract-module-statements
exampleTickerEngine : TickerEngine := mkEngine@{
    name := "ticker";
    behaviour := tickerBehaviour;
    initEnv := zeroTickerEnvironment;
  };
```
<!-- --8<-- [end:example-ticker-engine] -->
where `zeroTickerEnvironment` is defined as follows:

--8<-- "./docs/arch/node/engines/ticker_environment.juvix.md:environment-example"

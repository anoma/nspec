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
    ```

## Overview

There are only two messag tags:
`Increment`, which increases the counter state of the ticker,
and `Count`, which the ticker responds to with the current counter state.

## Mailbox states

The [[Ticker engine family|ticker]] does not rely on mailbox-relative state.

```juvix
syntax alias TickerMailboxState := Unit;
```

## Local state

The local state of the [[Ticker engine family|ticker]] is a counter,
storing a non-negative interger value.

```juvix
type TickerLocalState : Type := mkTickerLocalState {
  counter : Nat
};
```

## Timer Handle

The [[Ticker engine family|ticker]] does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

```juvix
syntax alias TickerTimerHandle := Unit;
```


```juvix
type TickerEnvironment : Type :=
  EngineEnvironment
    TickerLocalState
    TickerMsg
    TickerMailboxState
    TickerTimerHandle;
```
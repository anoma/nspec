---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-behaviour
tags:
- ticker
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.ticker_messages;
    ```

# Ticker Messages

## Message interface

<!-- --8<-- [start:TickerMsg] -->
```juvix
type TickerMsg :=
    | -- --8<-- [start:Increment]
    Increment
    -- --8<-- [end:Increment]
    | -- --8<-- [start:Count]
    Count
    -- --8<-- [end:Count]
```
<!-- --8<-- [end:TickerMsg] -->


There are only two message tags: `Increment`, which increases the counter state
of the ticker, and `Count`, which the ticker responds to with the current
counter state.

### `Increment` message

!!! quote "Increment"

    ```
    --8<-- "./ticker_messages.juvix.md:Increment"
    ```

An `Increment` message instructs the engine to increase the counter. This
message doesn't require any arguments.

### `Count` message

!!! quote "Count"

    ```
    --8<-- "./ticker_messages.juvix.md:Count"
    ```

A `Count` message requests the engine to send the current counter value back to
the requester. This message doesn't require any arguments.

## Message sequence diagrams

### Ticker Interaction Diagram

This diagram represents a simple interaction between a `Ticker` engine instance
and another entity sending increment requests and count requests.

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Ticker
    participant EngineTickerClient

    EngineTickerClient ->> Ticker: Send Increment
    Note over Ticker: Counter = 1

    EngineTickerClient ->> Ticker: Send Increment
    Note over Ticker: Counter = 2

    EngineTickerClient ->> Ticker: Send Count
    Ticker ->> EngineTickerClient: Respond with Counter (2)
```

<figcaption markdown="span">
A client interacts with the `Ticker` engine, which increments and responds with the counter value.
</figcaption>
</figure>

---
icon: material/message-draw
search:
  exclude: false
tags:
  - node-architecture
  - example
  - engine
  - ticker
  - message-types
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.ticker_messages;
    import prelude open;
    ```

# Ticker Messages

## Message interface

--8<-- "./ticker_messages.juvix.md:TickerMsg"

---

## Message sequence diagram

---

### Requesting a counter value

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Ticker
    participant EngineTickerClient

    EngineTickerClient ->> Ticker: Send TickerMsgIncrement
    Note over Ticker: Counter = 1

    EngineTickerClient ->> Ticker: Send TickerMsgIncrement
    Note over Ticker: Counter = 2

    EngineTickerClient ->> Ticker: Send TickerMsgCount
    Ticker ->> EngineTickerClient: Respond with Counter (2)
```

<figcaption markdown="span">
A client interacts with the `Ticker` engine, which increments and responds with the counter value.
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->

---

## Message types

---

### `TickerMsgIncrement`

A `TickerMsgIncrement` message instructs the engine to increase the counter.
This message doesn't require any arguments.

---

### `TickerMsgCountRequest`

A `TickerMsgCountRequest` message requests the engine to send the current counter value back to
the requester. This message doesn't require any arguments.

---

### `CountReply`

The `CountReply` payload contains the counter value.

```juvix
type CountReply : Type :=
  mkCountReply {
    counter : Nat;
  }
```

???+ quote "Arguments"

    `counter`
    : The counter value.

---

### `TickerMsg`

<!-- --8<-- [start:TickerMsg] -->
```juvix
type TickerMsg :=
  | TickerMsgIncrement
  | TickerMsgCountRequest
  | TickerMsgCountReply CountReply
```
<!-- --8<-- [end:TickerMsg] -->

---

## Engine components

- [[Ticker Configuration]]
- [[Ticker Environment]]
- [[Ticker Behaviour]]

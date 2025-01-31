---
icon: material/message-draw
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - wall-clock-engine
  - message-types
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.wall_clock_messages;
    import prelude open;
    ```

# Wall Clock Messages

These are the messages that the Wall Clock engine can receive/respond to.

## Message interface

--8<-- "./wall_clock_messages.juvix.md:WallClockMsg"


## Message sequence diagrams

---

### Wall Clock request and response

<!-- --8<-- [start:message-sequence-diagram-gettime] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant WallClockClient
    participant WallClock

    WallClockClient ->> WallClock: WallClockGetTime
    WallClock ->> WallClockClient: WallClockGetTimeResult
```

<figcaption markdown="span">
Sequence diagram: Wall Clock time request & response
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-gettime] -->

---

## Message types

??? code "Auxiliary Juvix code"

    ```juvix
    syntax alias StorageKey := String;
    syntax alias StorageValue := String;
    syntax alias EpochTimestamp := Nat;
    ```

---

### `WallClockGetTime`

A `WallClockGetTime` message tracks and manages time within the
local computing environment. This message doesn't require any
arguments.

### `TimeResult`

Reply to a `WallClockGetTime` request.

<!-- --8<-- [start:TimeResult] -->
```juvix
type TimeResult :=
  mkTimeResult {
    epochTime : EpochTimestamp;
  }
```
<!-- --8<-- [end:TimeResult] -->

???+ code "Arguments"

    `epochTime`
    : The current time in epoch format (seconds/milliseconds since epoch)

---

### `WallClockMsg`

<!-- --8<-- [start:WallClockMsg] -->
```juvix
type WallClockMsg :=
  | WallClockGetTime
  | WallClockGetTimeResult TimeResult
  ;
```
<!-- --8<-- [end:WallClockMsg] -->

---

## Engine components

- [[Wall Clock Configuration]]
- [[Wall Clock Environment]]
- [[Wall Clock Behaviour]]
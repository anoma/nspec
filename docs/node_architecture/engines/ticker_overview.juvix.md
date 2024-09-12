---
icon: octicons/container-24
search:
  exclude: false
tags:
  - engine-family
  - example
  - ticker
  - Juvix
---


!!! warning

    This page is still under construction, needs to be updated with the latest
    changes in the engine family type.

??? info "Juvix imports"

    ```juvix
    module node_architecture.engines.ticker_overview;
      import node_architecture.basics open;
      import node_architecture.types.engine_family as EngineFamily;
      open EngineFamily using {
          Engine;
          EngineEnvironment;
          EngineFamily;
          mkEngine;
          mkEngineEnvironment;
          mkEngineFamily
      };
    open EngineFamily.EngineEnvironment;
    import node_architecture.engines.ticker_environment open public;
    import node_architecture.engines.ticker_dynamics open public;
    ```

# Ticker Family Engine

## Purpose

A ticker engine, part of the `Ticker` engine family, maintains a counter in its
local state. This engine increases the counter whenever it gets a `Increment` message
and provides the updated result upon receiving a `Count` message. The initial
state initialises the counter.

## Components

??? quote "Local Environment"

    Source: [[Ticker Engine Environment]]

    ---8<--- "node_architecture/engines/ticker_environment.juvix.md"

??? quote "Guarded Actions"

    Source: [[Ticker Engine Dynamics]]

    ---8<--- "node_architecture/engines/ticker_dynamics.juvix.md"


## Engine Family

The engine family is defined by first establishing a
type synonym for the corresponding engine family type to
simplify the presentation.

!!! todo "fix the code"

```
EngineFamilyType : Type :=
  EngineFamily
    LocalStateType
    IMessageType
    MailboxStateType
    TimerHandleType
    GuardReturnType
    OMessageType
    SpawnEngineType;
```

So a `Ticker` engine family is defined as follows:

```
TickerFamily : EngineFamilyType
  := mkEngineFamily@{ actions := [incrementCounter; respondWithCounter];
};
```

As an example of an engine instance in this family, we could
define the ticker starting in zero. We, again, define for shorten presentation, the
corresponding engine instance type.

```
EngineInstanceType : Type :=
  Engine
    LocalStateType
    IMessageType
    MailboxStateType
    TimerHandleType
    GuardReturnType
    OMessageType
    SpawnEngineType;
```

Then, we define a `Ticker` engine instance as follows that set
the counter to zero:

```
zeroTicker : EngineInstanceType
  := mkEngine@{
    name := Left "TickerOne";
    family := TickerFamily;
    initEnv := mkEngineEnvironment@{
        localState := mkLocalStateType@{
            counter := 0;
        };
        name := Left  "TickerOne";
        timers := [];
        acquaintances := Set.empty;
        mailboxCluster := Map.empty;
    };
  } ;
```


## Interaction Diagrams

The figure below represents a simple interaction between two engine instances, a
`Ticker` engine instance and another entity sending increment requests and count
requests:

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

## Conversation-partner Diagram

<figure markdown="span">

```mermaid
erDiagram
  EngineTickerClient }o--|| Ticker: Increment
  EngineTickerClient ||--o{ Ticker: Count
```

<figcaption markdown="span">
The conversation-partner diagram shows the interactions between the `Ticker` engine and a client.
</figcaption>

</figure>

## Messages

```juvix
type TickerMessage := Increment | Count;
```

### Increment

An `Increment` message instructs the engine to increase the counter.

### Count

A `Count` message requests the engine to send
the current counter value back to the requester.

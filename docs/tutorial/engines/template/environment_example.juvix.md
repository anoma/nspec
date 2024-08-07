---
icon: octicons/check-24
search:
  exclude: false
---

# Ticker Environment

??? note "Juvix preamble" 

    ```juvix
    module tutorial.engines.Templates.EnvironmentExample;
    import node_architecture.basics open;
    import node_architecture.types.EngineFamily as EngineFamily;
    open EngineFamily using {
        Engine;
        EngineEnvironment;
        EngineFamily;
        mkActionInput;
        mkActionResult;
        mkEngine;
        mkEngineEnvironment;
        mkEngineFamily;
        mkGuardedAction
    };
    open EngineFamily.EngineEnvironment;
    ```

## Overview

There are only two messag tags:
`Increment`, which increases the counter state
and `Count`, which is responded to with
the current counter state.

### Messages

!!! note "TickerMessage data type"

    ```juvix
    type TickerMessage := Increment | Count;
    ```

#### Increment

An `Increment` message instructs the engine to increase the counter.


#### Count

A `Count` message requests the engine to send
the current counter value back to the requester.


## Mailbox State

Engine families often requires various types to represent the potential states
of their mailboxes. However, in this specific case, the `Ticker` engine does not
necessitate any mailbox states. As a result, we define the mailbox state type as
`Unit` using the Juvix alias syntax.

```juvix
syntax alias MailboxStateType := Unit;
```

## Timer Handle

The `Ticker` engine does not require a timer handle. Therefore, we define the
timer handle type as `Unit`.

```juvix
syntax alias TimerHandleType := Unit;
```

#### Local State

Given the types for the local state and messages, we inherently possess the type
of the engine environment. Nonetheless, to ensure clarity, let us define it
explicitly using the `Environment` type.

```juvix
EnvType : Type := 
  EngineFamily.EngineEnvironment 
    LocalStateType 
    TickerMessage
    MailboxStateType
    TimerHandleType;
```

## Ticker Local Environment

### Local State Type

The local state of the `Ticker` includes:

- **counter**: An integer value representing the current counter state.

```juvix
type LocalStateType : Type := mkLocalStateType {
  counter : Nat
};
```


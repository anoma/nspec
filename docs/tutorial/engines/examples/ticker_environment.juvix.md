---
icon: octicons/project-template-24
search:
  exclude: false
tags:
  - engine-family
  - example
  - ticker
  - Juvix
---


??? info "Juvix imports"

    ```juvix
    module tutorial.engines.examples.ticker_environment;

    import node_architecture.basics open;
    import node_architecture.types.engine_family as EngineFamily;
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

# Ticker Local Environment

## Local State Type

The local state of the `Ticker` includes:

- **counter**: An integer value representing the current counter state.

```juvix
type LocalStateType : Type := mkLocalStateType {
  counter : Nat
};
```

### Message Types

### Incoming Message Type

The `Ticker` processes the following message types:

- **Increment**: A message that instructs the engine to increase the counter.
- **Count**: A message requesting the engine to send back the current counter
  value.

```juvix
type IMessageType := Increment | Count;
```

### Outgoing Message Type

To respond to the `Count` message, the engine sends a message containing the
current counter value.

```juvix
type OMessageType := Result Nat;
```

## Mailbox States Types

Engine families often requires various types to represent the potential states
of their mailboxes. However, in this specific case, the `Ticker` engine does not
necessitate any mailbox states. As a result, we define the mailbox state type as
`Unit` using the Juvix alias syntax.

```juvix
syntax alias MailboxStateType := Unit;
```

## Timer Handle Type

The `Ticker` engine does not require a timer handle. Therefore, we define the
timer handle type as `Unit`.

```juvix
syntax alias TimerHandleType := Unit;
```

#### Local Environment Type

Given the types for the local state and messages, we inherently possess the type
of the engine environment. Nonetheless, to ensure clarity, let us define it
explicitly using the `Environment` type.

```juvix
EnvType : Type :=
  EngineFamily.EngineEnvironment
    LocalStateType
    IMessageType
    MailboxStateType
    TimerHandleType;
```
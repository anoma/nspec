---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - router
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.router_environment;

    import arch.node.engines.router_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Router Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

<!-- --8<-- [start:RouterMailboxState] -->
```juvix
RouterMailboxState : Type := Unit;
```
<!-- --8<-- [start:RouterMailboxState] -->

## Local state

<!-- --8<-- [start:RouterLocalState] -->
```juvix
type RouterLocalState :=
  mkRouterLocalState;
```
<!-- --8<-- [end:RouterLocalState] -->

## Timer handles

<!-- --8<-- [start:RouterTimerHandle] -->
```juvix
RouterTimerHandle : Type := Unit;
```
<!-- --8<-- [end:RouterTimerHandle] -->

## Timestamped Trigger

<!-- --8<-- [start:RouterTimestampedTrigger] -->
```juvix
RouterTimestampedTrigger : Type :=
  TimestampedTrigger
    RouterTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:RouterTimestampedTrigger] -->

## The Router Environment

### `RouterEnv`

<!-- --8<-- [start:RouterEnv] -->
```juvix
RouterEnv : Type :=
  EngineEnv
    RouterLocalState
    RouterMailboxState
    RouterTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:RouterEnv] -->

#### Instantiation

<!-- --8<-- [start:exRouterEnv] -->
```juvix extract-module-statements
module router_environment_example;

exRouterEnv : RouterEnv :=
  mkEngineEnv@{
    localState := mkRouterLocalState;
    mailboxCluster := Map.empty;
    acquaintances := Set.empty;
    timers := []
  };

end;
```
<!-- --8<-- [end:exRouterEnv] -->

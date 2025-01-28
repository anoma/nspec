---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- executor-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.executor_messages;
    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    ```

# Executor Messages

These are the specific messages that the Executor engine can receive/respond to.

## Message interface

--8<-- "./executor_messages.juvix.md:ExecutorMsg"

## Message sequence diagram

---

### Execution flow

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
    participant Executor
    participant Shard
    participant Worker

    Executor->>Shard: KVSReadRequest
    Shard->>Executor: KVSRead
    Executor->>Shard: KVSWrite
    Executor->>Worker: ExecutorFinished
```

<figcaption markdown="span">
Basic execution flow sequence showing interaction with shards and completion notification
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->

---

## Message types

---

### `ExecutorFinishedMsg`

Notification that execution is complete.

<!-- --8<-- [start:ExecutorFinishedMsg] -->
```juvix
type ExecutorFinishedMsg : Type :=
  mkExecutorFinishedMsg {
    success : Bool;
    values_read : List (Pair KVSKey KVSDatum);
    values_written : List (Pair KVSKey KVSDatum)
  }
```
<!-- --8<-- [end:ExecutorFinishedMsg] -->

---

???+ quote "Arguments"

    `success`
    : Whether execution completed successfully

    `values_read`
    : List of all key-value pairs that were read

    `values_written`
    : List of all key-value pairs that were written

---

### `ExecutorMsg`

<!-- --8<-- [start:ExecutorMsg] -->
```juvix
type ExecutorMsg :=
  | ExecutorMsgExecutorFinished ExecutorFinishedMsg
  ;
```
<!-- --8<-- [end:ExecutorMsg] -->

---

## Engine components

- [[Executor Configuration]]
- [[Executor Environment]]
- [[Executor Behaviour]]
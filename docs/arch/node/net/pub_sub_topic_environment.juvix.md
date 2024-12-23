---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- pub-sub-topic-engine
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.pub_sub_topic_environment;

    import arch.node.net.pub_sub_topic_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Pub/Sub Topic Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

### `PubSubTopicMailboxState`

<!-- --8<-- [start:PubSubTopicMailboxState] -->
```juvix
PubSubTopicMailboxState : Type := Unit;
```
<!-- --8<-- [end:PubSubTopicMailboxState] -->

## Local state

### `PubSubTopicLocalState`

<!-- --8<-- [start:PubSubTopicLocalState] -->
```juvix
type PubSubTopicLocalState :=
  mkPubSubTopicLocalState;
```
<!-- --8<-- [end:PubSubTopicLocalState] -->

## Timer handles

### `PubSubTopicTimerHandle`

<!-- --8<-- [start:PubSubTopicTimerHandle] -->
```juvix
PubSubTopicTimerHandle : Type := Unit;
```
<!-- --8<-- [end:PubSubTopicTimerHandle] -->

### `PubSubTopicTimestampedTrigger`

<!-- --8<-- [start:PubSubTopicTimestampedTrigger] -->
```juvix
PubSubTopicTimestampedTrigger : Type :=
  TimestampedTrigger
    PubSubTopicTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:PubSubTopicTimestampedTrigger] -->

## Engine Environment

### `PubSubTopicEnv`

<!-- --8<-- [start:PubSubTopicEnv] -->
```juvix
PubSubTopicEnv : Type :=
  EngineEnv
    PubSubTopicLocalState
    PubSubTopicMailboxState
    PubSubTopicTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:PubSubTopicEnv] -->

#### Instantiation

<!-- --8<-- [start:exPubSubTopicEnv] -->
```juvix extract-module-statements
module pub_sub_topic_environment_example;

exPubSubTopicEnv : PubSubTopicEnv :=
  mkEngineEnv@{
    localState := mkPubSubTopicLocalState;
    mailboxCluster := Map.empty;
    acquaintances := Set.empty;
    timers := []
  };

end;
```
<!-- --8<-- [end:exPubSubTopicEnv] -->

---
icon: octicons/gear-16
search:
  exclude: false
tags:
- engines
- conventions
---

??? note "Juvix preamble"

    ```juvix
    module arch.node.engines.topic;

    import prelude open;
    import arch.node.net.topic_messages open;
    -- TODO import arch.node.net.topic_environment open;
    -- TODO import arch.node.net.topic_behaviour open;
    import arch.node.types.engine open;
    open environment_example;
    ```

# Topic Engine

## Purpose

--8<-- [start:purpose]
The *Topic* engine is responsible
for topic-based publish/subscribe (pub/sub) message dissemination
for one specific pub/sub topic.

It allows a set of authorized publishers
to publish messages in the topic,
and allows local and remote engines to subscribe to it.
Published messages are disseminated to all subscribers.

The engine instance name corresponds to the `TopicID`.
--8<-- [end:purpose]

## Components

- [[Topic Messages]]
- [[Topic Environment]]
- [[Topic Behaviour]]

## Useful links

- Some
- Useful
- Links

## Types

### `TopicEngine`

<!-- --8<-- [start:TopicEngine] -->
```TODO juvix
TopicEngine : Type :=
  Engine
    TopicLocalState
    TopicMailboxState
    TopicTimerHandle
    TopicMatchableArgument
    TopicActionLabel
    TopicPrecomputation;
```
<!-- --8<-- [end:TopicEngine] -->

#### Example of a pubsub engine

<!-- --8<-- [start:TopicEngine] -->
```TODO juvix
exampleTopicEngine : TopicEngine := mkEngine@{
  name := "<topic_id>";
  behaviour := topicBehaviour;
  initEnv := topicEnvironmentExample;
};
```
<!-- --8<-- [end:TopicEngine] -->

where `topicEnvironmentExample` is defined as follows:

--8 TODO <-- "./docs/arch/node/net/environment.juvix.md:environment-example"

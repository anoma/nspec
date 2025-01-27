---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- pub-sub-topic-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.pub_sub_topic;

    import arch.node.engines.pub_sub_topic_messages open public;
    import arch.node.engines.pub_sub_topic_config open public;
    import arch.node.engines.pub_sub_topic_environment open public;
    import arch.node.engines.pub_sub_topic_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open pub_sub_topic_config_example;
    open pub_sub_topic_environment_example;
    open pub_sub_topic_behaviour_example;
    ```

# Pub/Sub Topic Engine

## Purpose

<!-- --8<-- [start:purpose] -->
A *Pub/Sub Topic* engine is responsible
for topic-based publish/subscribe (pub/sub) message dissemination
for a single pub/sub topic.

The protocol allows
a set of authorized publishers to publish messages in the topic,
as well as local and remote engines to subscribe to it.
Published messages are disseminated to all subscribers.

The engine instance name corresponds to the `TopicID`.
<!-- --8<-- [end:purpose] -->

## Components

- [[Pub/Sub Topic Messages]]
- [[Pub/Sub Topic Configuration]]
- [[Pub/Sub Topic Environment]]
- [[Pub/Sub Topic Behaviour]]

## Type

<!-- --8<-- [start:PubSubTopicEngine] -->
```juvix
PubSubTopicEngine : Type :=
  Engine
    PubSubTopicLocalCfg
    PubSubTopicLocalState
    PubSubTopicMailboxState
    PubSubTopicTimerHandle
    PubSubTopicActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:PubSubTopicEngine] -->

### Instantiation

<!-- --8<-- [start:exPubSubTopicEngine] -->
```juvix
exPubSubTopicEngine : PubSubTopicEngine :=
  mkEngine@{
    cfg := exPubSubTopicCfg;
    env := exPubSubTopicEnv;
    behaviour := exPubSubTopicBehaviour;
  };
```
<!-- --8<-- [end:exPubSubTopicEngine] -->

Where `exPubSubTopicCfg` is defined as follows:

--8<-- "./pub_sub_topic_config.juvix.md:exPubSubTopicCfg"

`exPubSubTopicEnv` is defined as follows:

--8<-- "./pub_sub_topic_environment.juvix.md:exPubSubTopicEnv"

and `exPubSubTopicBehaviour` is defined as follows:

--8<-- "./pub_sub_topic_behaviour.juvix.md:exPubSubTopicBehaviour"

---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - pub-sub-topic
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.pub_sub_topic_config;

    import arch.node.engines.pub_sub_topic_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Pub/Sub Topic Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## Local Configuration

### `PubSubTopicLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:PubSubTopicLocalCfg] -->
```juvix
type PubSubTopicLocalCfg :=
  mk;
```
<!-- --8<-- [end:PubSubTopicLocalCfg] -->

## Engine Configuration

### `PubSubTopicCfg`

<!-- --8<-- [start:PubSubTopicCfg] -->
```juvix
PubSubTopicCfg : Type :=
  EngineCfg
    PubSubTopicLocalCfg;
```
<!-- --8<-- [end:PubSubTopicCfg] -->

## Instantiation

<!-- --8<-- [start:exPubSubTopicCfg] -->
```juvix extract-module-statements
module pub_sub_topic_config_example;

exPubSubTopicCfg : PubSubTopicCfg :=
  EngineCfg.mk@{
    node := PublicKey.Curve25519PubKey "0xabcd1234";
    name := "pub-sub-topic";
    cfg := PubSubTopicLocalCfg.mk;
  };

end;
```
<!-- --8<-- [end:exPubSubTopicCfg] -->

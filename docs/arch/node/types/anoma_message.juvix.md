---
icon: material/message-text
search:
  exclude: false
tags:
  - node-architecture
  - types
  - engine
  - message-types
  - prelude
---

??? code "Juvix imports"

    ```juvix
    module arch.node.types.anoma_message;

    import prelude open;
    import arch.system.state.resource_machine.notes.nockma open;

    {- Identity -}

    import arch.node.engines.identity_management_messages open;
    import arch.node.engines.decryption_messages open;
    import arch.node.engines.encryption_messages open;
    import arch.node.engines.commitment_messages open;

    import arch.node.engines.verification_messages open;
    import arch.node.engines.reads_for_messages open;
    import arch.node.engines.signs_for_messages open;
    import arch.node.engines.naming_messages open;

    import arch.node.engines.local_key_value_storage_messages open;
    import arch.node.engines.logging_messages open;
    import arch.node.engines.wall_clock_messages open;
    import arch.node.engines.local_time_series_storage_messages open;

    {- Network -}

    import arch.node.engines.net_registry_messages open;
    import arch.node.engines.router_messages open;
    import arch.node.engines.transport_protocol_messages open;
    import arch.node.engines.transport_connection_messages open;
    import arch.node.engines.pub_sub_topic_messages open;
    import arch.node.engines.storage_messages open;

    {- Ordering -}

    import arch.node.engines.mempool_worker_messages open;
    import arch.node.engines.executor_messages open;
    import arch.node.engines.shard_messages open;

    {- Misc -}

    import arch.node.engines.ticker_messages open;

    {- Templates -}

    import tutorial.engines.template_messages open;
    import tutorial.engines.template_minimum_messages open;

    -- Add imports here
    ```

# Anoma Message

The _Anoma_ message type contains all admissible messages that can be sent
between nodes in the network. An Anoma message is of the type `Msg`. Each
constructor of the type `Msg` corresponds to a specific type of message comming
from a specific engine. For example, the engine `TickerEngine` has a
corresponding message type `TickerMsg`.

<!-- --8<-- [start:Msg] -->
```juvix
type Msg :=

  {- Identity -}

  | IdentityManagement IdentityManagementMsg
  | Decryption DecryptionMsg
  | Encryption EncryptionMsg
  | Commitment CommitmentMsg

  | Verification VerificationMsg
  | ReadsFor ReadsForMsg
  | SignsFor SignsForMsg
  | Naming NamingMsg

  | LocalKVStorage LocalKVStorageMsg
  | Logging LoggingMsg
  | WallClock WallClockMsg
  | LocalTSStorage LocalTSStorageMsg

  {- Network -}

  | Router (RouterMsg Msg)
  | TransportProtocol TransportProtocolMsg
  | TransportConnection TransportConnectionMsg
  | PubSubTopic PubSubTopicMsg
  | Storage StorageMsg

  {- Ordering -}

  | MempoolWorker (MempoolWorkerMsg Noun)
  | Executor ExecutorMsg
  | Shard ShardMsg

  {- Misc -}

  | Ticker TickerMsg

  {- Templates -}

  | Template TemplateMsg
  | TemplateMinimum TemplateMinimumMsg

  -- Add more messages here
  ;
```
<!-- --8<-- [end:Msg] -->

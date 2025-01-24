---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Anoma-Message
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_message;

    import prelude;

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

    import arch.node.net.router_messages open;
    import arch.node.net.node_proxy_messages open;
    import arch.node.net.transport_protocol_messages open;
    import arch.node.net.transport_connection_messages open;
    import arch.node.net.pub_sub_topic_messages open;
    import arch.node.net.storage_messages open;

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

The _Anoma_ message type `Msg` contains all admissible messages that can be sent
between nodes in the network. Each
constructor of the type `Msg` corresponds to a specific type of message comming
from a specific engine. For example, the engine `TickerEngine` has a
corresponding message type `TickerMsg`.

<!-- --8<-- [start:Msg] -->
```juvix
type Msg :=

  {- Identity -}

  | MsgIdentityManagement IdentityManagementMsg
  | MsgDecryption DecryptionMsg
  | MsgEncryption EncryptionMsg
  | MsgCommitment CommitmentMsg

  | MsgVerification VerificationMsg
  | MsgReadsFor ReadsForMsg
  | MsgSignsFor SignsForMsg
  | MsgNaming NamingMsg

  | MsgLocalKVStorage LocalKVStorageMsg
  | MsgLogging LoggingMsg
  | MsgWallClock WallClockMsg
  | MsgLocalTSStorage LocalTSStorageMsg

  {- Network -}

  | MsgRouter (RouterMsg Msg)
  | MsgNodeProxy (NodeProxyMsg Msg)
  | MsgTransportProtocol TransportProtocolMsg
  | MsgTransportConnection TransportConnectionMsg
  | MsgPubSubTopic PubSubTopicMsg
  | MsgStorage StorageMsg

  {- Ordering -}

  | MsgMempoolWorker MempoolWorkerMsg
  | MsgExecutor ExecutorMsg
  | MsgShard ShardMsg

  {- Misc -}

  | MsgTicker TickerMsg

  {- Templates -}

  | MsgTemplate TemplateMsg
  | MsgTemplateMinimum TemplateMinimumMsg

  -- Add more messages here
  ;
```
<!-- --8<-- [end:Msg] -->

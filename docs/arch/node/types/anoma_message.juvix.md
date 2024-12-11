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

    {- Examples -}

    import arch.node.example.template_messages open using {TemplateMsg};
    import arch.node.example.ticker_messages open using {TickerMsg};

    {- Identity -}

    import arch.node.engines.identity_management_messages open using {IdentityManagementMsg};
    import arch.node.engines.decryption_messages open using {DecryptionMsg};
    import arch.node.engines.encryption_messages open using {EncryptionMsg};
    import arch.node.engines.commitment_messages open using {CommitmentMsg};

    import arch.node.engines.verification_messages open using {VerificationMsg};
    import arch.node.engines.reads_for_messages open using {ReadsForMsg};
    import arch.node.engines.signs_for_messages open using {SignsForMsg};
    import arch.node.engines.naming_messages open using {NamingMsg};

    import arch.node.engines.local_key_value_storage_messages open using {LocalKVStorageMsg};
    import arch.node.engines.logging_messages open using {LoggingMsg};
    import arch.node.engines.wall_clock_messages open using {WallClockMsg};
    import arch.node.engines.local_time_series_storage_messages open using {LocalTSStorageMsg};

    {- Network -}

    import arch.node.net.router_messages open;
    import arch.node.net.node_proxy_messages open;
    import arch.node.net.transport_protocol_messages open;
    import arch.node.net.transport_connection_messages open;
    import arch.node.net.pub_sub_topic_messages open;
    import arch.node.net.storage_messages open;

    {- Ordering -}

    import arch.node.engines.mempool_worker_messages open using {MempoolWorkerMsg};
    import arch.node.engines.executor_messages open using {ExecutorMsg};
    import arch.node.engines.shard_messages open using {ShardMsg};
    ```

# Anoma Message

The _Anoma_ message type contains all admissible messages
that can be sent between nodes in the network.
An Anoma message is of the type `Msg`.
Each constructor of the type `Msg`
corresponds to a specific type of message comming from a specific engine.
For example, the engine `TickerEngine`
has a corresponding message type `TickerMsg`.

<!-- --8<-- [start:anoma-messages-type] -->
```juvix
type Msg :=
  {- Examples -}

  | MsgTemplate TemplateMsg
  | MsgTicker TickerMsg

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
  ;
```
<!-- --8<-- [end:anoma-messages-type] -->

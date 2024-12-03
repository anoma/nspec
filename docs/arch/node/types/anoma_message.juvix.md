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

    import arch.node.engines.template_messages open using {TemplateMsg};
    import arch.node.engines.ticker_messages open using {TickerMsg};

    import arch.node.engines.commitment_messages open using {CommitmentMsg};
    import arch.node.engines.identity_management_messages open using {IdentityManagementMsg};
    import arch.node.engines.decryption_messages open using {DecryptionMsg};
    import arch.node.engines.encryption_messages open using {EncryptionMsg};

    import arch.node.engines.verification_messages open using {VerificationMsg};
    import arch.node.engines.reads_for_messages open using {ReadsForMsg};
    import arch.node.engines.signs_for_messages open using {SignsForMsg};
    import arch.node.engines.naming_messages open using {NamingMsg};

    import arch.node.engines.local_key_value_storage_messages open using {LocalKVStorageMsg};
    import arch.node.engines.logging_messages open using {LoggingMsg};
    import arch.node.engines.wall_clock_messages open using {WallClockMsg};
    import arch.node.engines.local_time_series_storage_messages open using {LocalTSStorageMsg};

    import arch.node.engines.shard_2_messages open using {ShardMsg};
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
  | MsgTemplate TemplateMsg
  | MsgTicker TickerMsg
  | MsgCommitment CommitmentMsg
  | MsgIdentityManagement IdentityManagementMsg
  | MsgDecryption DecryptionMsg
  | MsgEncryption EncryptionMsg
  | MsgVerification VerificationMsg
  | MsgReadsFor ReadsForMsg
  | MsgSignsFor SignsForMsg
  | MsgNaming NamingMsg
  | MsgLocalKVStorage LocalKVStorageMsg
  | MsgLogging LoggingMsg
  | MsgWallClock WallClockMsg
  | MsgLocalTSStorage LocalTSStorageMsg
  | MsgShard ShardMsg
  ;
```
<!-- --8<-- [end:anoma-messages-type] -->

---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Anoma-Message
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_message;

{- Examples -}
    import arch.node.engines.template_messages open using {TemplateMsg};
    import arch.node.engines.ticker_messages open using {TickerMsg};

{- Identity -}
--    import arch.node.engines.identity_management_messages open using {IdentityManagementMsg};
--    import arch.node.engines.decryption_messages open using {DecryptionMsg};
--    import arch.node.engines.encryption_messages open using {EncryptionMsg};
--    import arch.node.engines.commitment_messages open using {CommitmentMsg};
--    import arch.node.engines.verification_messages open using {VerificationMsg};
--    import arch.node.engines.reads_for_messages open using {ReadsForMsg};
--    import arch.node.engines.signs_for_messages open using {SignsForMsg};
--    import arch.node.engines.naming_messages open using {NamingMsg};

{- Network -}
    import arch.node.net.router_messages open;
    import arch.node.net.node_proxy_messages open;
    import arch.node.net.transport_messages open;
    import arch.node.net.topic_messages open;
    import arch.node.net.storage_messages open;
    ```

# Anoma Message

The _Anoma_ message type contains all admissible messages
that can be sent between nodes in the network.
An Anoma message is of the type `Msg`.
Each constructor of the type `Msg` corresponds to a specific type of message coming from a specific engine.
For example, the engine family `Ticker` has a corresponding message type `TickerMsg`.

<!-- --8<-- [start:anoma-messages-type] -->
```juvix
type Msg :=
{- Examples -}
  | MsgTemplate TemplateMsg
  | MsgTicker TickerMsg

{- Identity -}
--  | MsgIdentityManagement IdentityManagementMsg
--  | MsgDecryption DecryptionMsg
--  | MsgEncryption EncryptionMsg
--  | MsgCommitment CommitmentMsg
--  | MsgVerification VerificationMsg
--  | MsgReadsFor ReadsForMsg
--  | MsgSignsFor SignsForMsg
--  | MsgNaming NamingMsg

{- Network -}
  | MsgRouter RouterMsg
  | MsgNodeProxy NodeProxyMsg
  | MsgTransport TransportMsg
  | MsgTopic TopicMsg
  | MsgStorage StorageMsg
  ;
```
<!-- --8<-- [end:anoma-messages-type] -->

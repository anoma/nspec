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
    module node_architecture.types.anoma_message;
    import node_architecture.basics open;
    import node_architecture.engines.ticker_overview open using {TickerMsg};
    import node_architecture.engines.identity_management_overview open using {IdentityManagementMsg};
    import node_architecture.engines.decryption_overview open using {DecryptionMsg};
    import node_architecture.engines.encryption_overview open using {EncryptionMsg};
    import node_architecture.engines.commitment_overview open using {CommitmentMsg};
    import node_architecture.engines.verification_overview open using {VerificationMsg};
    import node_architecture.engines.reads_for_overview open using {ReadsForMsg};
    import node_architecture.engines.signs_for_overview open using {SignsForMsg};
    import node_architecture.engines.naming_overview open using {NamingMsg};
    ```

# Anoma Messages

An _Anoma_ message is a admissible messages that can be sent between nodes in
the network. An Anoma message is of the type `Msg`. Each constructor of the type
`Msg` corresponds to a specific type of message comming from a specific engine
family. For example, the engine family `Ticker` has a corresponding message type
`TickerMsg`.

```juvix
type Msg :=
  | MsgTicker TickerMsg
  | MsgIdentityManagement IdentityManagementMsg
  | MsgDecryption DecryptionMsg
  | MsgEncryption EncryptionMsg
  | MsgCommitment CommitmentMsg
  | MsgVerification VerificationMsg
  | MsgReadsFor ReadsForMsg
  | MsgSignsFor SignsForMsg
  | MsgNaming NamingMsg
  ;
```
---
icon: material/chart-timeline-variant
search:
  exclude: false
tags:
  - simulator
  - visualizer
  - mermaid
---

# Simulation Message Visualizer

This module provides functions to generate Mermaid sequence diagrams from a list of engine messages, allowing for visualization of simulation traces.

??? code "Juvix Code"

    ```juvix
    module arch.node.integration.visualizer;
    
    import prelude open;
    import Stdlib.Data.Set as Set;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message open;
    import arch.system.state.resource_machine.notes.nockma open; -- For Noun type
    import arch.node.types.basics open; -- For TxFingerprint, KVSKey, KVSDatum etc.

    -- Imports from arch.node.types.anoma_message for detailed message types
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
    import arch.node.engines.net_registry_messages open;
    import arch.node.engines.router_messages open;
    import arch.node.engines.transport_protocol_messages open;
    import arch.node.engines.transport_connection_messages open;
    import arch.node.engines.pub_sub_topic_messages open;
    import arch.node.engines.storage_messages open;
    import arch.node.engines.mempool_worker_messages open;
    import arch.node.engines.executor_messages open;
    import arch.node.engines.shard_messages open;
    import arch.node.engines.ticker_messages open;
    import tutorial.engines.template_messages open;
    import tutorial.engines.template_minimum_messages open;
    
    -- Function to convert EngineID to a String for diagram labels
    engineIdToString (eid : EngineID) : String :=
      let
        nodeStr := case fst eid of {
          | none := "Client" -- Or some other placeholder for external senders
          | some (PublicKey.Curve25519PubKey pk) := pk -- Assuming NodeID is a string-like pubkey
        };
        engineNameStr := snd eid;
      in nodeStr ++str "/" ++str engineNameStr;
    
    -- Helper to join a list of strings with a separator
    terminating
    stringJoin (separator : String) (strings : List String) : String :=
      case strings of {
        | [] := ""
        | s :: [] := s
        | s :: rest := s ++str separator ++str (stringJoin separator rest)
      };
    
    -- Helper to get unique participants
    getParticipants (messages : List (EngineMsg Msg)) : Set String :=
      let
        addParticipantIds (msg : EngineMsg Msg) (acc : Set String) : Set String :=
          let
            senderStr := engineIdToString (EngineMsg.sender msg);
            targetStr := engineIdToString (EngineMsg.target msg);
          in insert senderStr (insert targetStr acc); -- Uses `insert` from prelude's Set import
      in foldr addParticipantIds Set.empty messages;
    
    -- Helper to convert Bool to String
    boolToString (b : Bool) : String := if | b := "true" | else := "false";
    
    -- Placeholder for Hash to String conversion (if needed)
    hashToString (h : Hash) : String := "<hash>"; -- Replace with actual conversion
    
    -- Placeholder for Noun to String conversion
    terminating
    nounToString (n : Noun) : String :=
      case n of {
        | Noun.Atom a := natToString a
        | Noun.Cell l r := "[" ++str (nounToString l) ++str " " ++str (nounToString r) ++str "]"
      };
    
    -- Placeholder for KVSKey to String conversion
    kvsKeyToString (key : KVSKey) : String :=
      "<KVSKeyPlaceholder>";
    
    -- Placeholder for KVSDatum to String conversion
    kvsDatumToString (datum : KVSDatum) : String :=
      "<KVSDatumPlaceholder>";
    
    -- Helper to convert TransactionLabel to String
    transactionLabelToString (label : TransactionLabel KVSKey KVSKey) : String :=
      let
        readKeysStr := stringJoin "," (map kvsKeyToString (TransactionLabel.read label));
        writeKeysStr := stringJoin "," (map kvsKeyToString (TransactionLabel.write label));
      in "R:[" ++str readKeysStr ++str "]W:[" ++str writeKeysStr ++str "]";
    
    -- Specific message type to string converters
    
    terminating
    mempoolWorkerMsgToString (mwMsg : MempoolWorkerMsg Noun) : String :=
      case mwMsg of {
        | MempoolWorkerMsg.TransactionRequest tr :=
          "TxReq(label: " ++str (transactionLabelToString (TransactionCandidate.label (TransactionRequest.tx tr))) ++str ")"
        | MempoolWorkerMsg.TransactionAck ack :=
          "TxAck(hash: " ++str (hashToString (TransactionAck.tx_hash ack)) ++str ", batch: " ++str (natToString (TransactionAck.batch_number ack)) ++str ")"
      };
    
    terminating
    shardMsgToString (sMsg : ShardMsg) : String :=
      case sMsg of {
        | ShardMsg.KVSReadRequest req :=
          "KVSReadReq(key:" ++str (kvsKeyToString (KVSReadRequestMsg.key req)) ++str ",ts:" ++str (natToString (KVSReadRequestMsg.timestamp req)) ++str ",act:" ++str (boolToString (KVSReadRequestMsg.actual req)) ++str ")"
        | ShardMsg.KVSWrite write :=
          let datumStr := case KVSWriteMsg.datum write of {
            | none := "<none>"
            | some d := kvsDatumToString d
          };
          in "KVSWrite(key:" ++str (kvsKeyToString (KVSWriteMsg.key write)) ++str ",ts:" ++str (natToString (KVSWriteMsg.timestamp write)) ++str ",data:" ++str datumStr ++str ")"
        | ShardMsg.KVSAcquireLock acquireLock :=
          "KVSAcquireLock(ts:" ++str (natToString (KVSAcquireLockMsg.timestamp acquireLock)) ++str ")"
        | ShardMsg.KVSLockAcquired lockAcquired :=
          "KVSLockAcquired(ts:" ++str (natToString (KVSLockAcquiredMsg.timestamp lockAcquired)) ++str ")"
        | ShardMsg.KVSRead readReply :=
          "KVSRead(key:" ++str (kvsKeyToString (KVSReadMsg.key readReply)) ++str ",ts:" ++str (natToString (KVSReadMsg.timestamp readReply)) ++str ",data:" ++str (kvsDatumToString (KVSReadMsg.data readReply)) ++str ")"
        | ShardMsg.UpdateSeenAll updateSeenAll :=
          "UpdateSeenAll(ts: " ++str (natToString (UpdateSeenAllMsg.timestamp updateSeenAll)) ++str ", write: " ++str (boolToString (UpdateSeenAllMsg.write updateSeenAll)) ++str ")"
      };
    
    terminating
    executorMsgToString (execMsg : ExecutorMsg) : String :=
      case execMsg of {
        | ExecutorMsg.ExecutorFinished fin :=
          "ExecFinished(ok: " ++str (boolToString (ExecutorFinishedMsg.success fin)) ++str ")" -- Simplified for now
      };
    
    terminating
    loggingMsgToString (logMsg : LoggingMsg) : String :=
      case logMsg of {
        | LoggingMsg.Append appendVal :=
          "LogAppend(val: \"" ++str (AppendValue.value appendVal) ++str "\")"
      };
    
    -- Placeholder helpers for identity types
    identityNameToString (idName : IdentityName) : String := "<IdentityName>";
    externalIdentityToString (extId : ExternalIdentity) : String := "<ExternalIdentity>";
    identityNameEvidenceToString (evidence : IdentityNameEvidence) : String := "<IdentityNameEvidence>";

    terminating
    namingMsgToString (nMsg : NamingMsg) : String :=
      case nMsg of {
        | NamingMsg.ResolveNameRequest req :=
          "ResolveNameReq(name:" ++str (identityNameToString (RequestResolveName.identityName req)) ++str ")"
        | NamingMsg.ResolveNameReply reply :=
          let count := length (Set.toList (ReplyResolveName.externalIdentities reply));
          in "ResolveNameReply(count:" ++str (natToString count) ++str ", err:" ++str (option (ReplyResolveName.err reply) "None" id) ++str ")"
        | NamingMsg.SubmitNameEvidenceRequest req :=
          "SubmitEvidenceReq(ev:" ++str (identityNameEvidenceToString (RequestSubmitNameEvidence.evidence req)) ++str ")"
        | NamingMsg.SubmitNameEvidenceReply reply :=
          "SubmitEvidenceReply(err:" ++str (option (ReplySubmitNameEvidence.err reply) "None" id) ++str ")"
        | NamingMsg.QueryNameEvidenceRequest req :=
          "QueryEvidenceReq(id:" ++str (externalIdentityToString (RequestQueryNameEvidence.externalIdentity req)) ++str ")"
        | NamingMsg.QueryNameEvidenceReply reply :=
          let evCount := length (Set.toList (ReplyQueryNameEvidence.evidence reply));
          in "QueryEvidenceReply(id:" ++str (externalIdentityToString (ReplyQueryNameEvidence.externalIdentity reply)) ++str ", evCount:" ++str (natToString evCount) ++str ", err:" ++str (option (ReplyQueryNameEvidence.err reply) "None" id) ++str ")"
      };
    
    -- Main dispatcher function for Msg to String
    terminating
    msgToString (actualMsg : Msg) : String :=
      case actualMsg of {
        | Msg.MempoolWorker mwMsg := mempoolWorkerMsgToString mwMsg
        | Msg.Shard shardMsg := shardMsgToString shardMsg
        | Msg.Executor execMsg := executorMsgToString execMsg
        -- Add other top-level Msg types from anoma_message.juvix.md
        -- Example placeholder, to be expanded with actual calls to specific xxxMsgToString functions
        | Msg.IdentityManagement _ := "IdentityManagementMsg"
        | Msg.Decryption _ := "DecryptionMsg"
        | Msg.Encryption _ := "EncryptionMsg"
        | Msg.Commitment _ := "CommitmentMsg"
        | Msg.Verification _ := "VerificationMsg"
        | Msg.ReadsFor _ := "ReadsForMsg"
        | Msg.SignsFor _ := "SignsForMsg"
        | Msg.Naming nMsg := namingMsgToString nMsg
        | Msg.LocalKVStorage _ := "LocalKVStorageMsg"
        | Msg.Logging logMsg := loggingMsgToString logMsg
        | Msg.WallClock _ := "WallClockMsg"
        | Msg.LocalTSStorage _ := "LocalTSStorageMsg"
        | Msg.Router _ := "RouterMsg"
        | Msg.TransportProtocol _ := "TransportProtocolMsg"
        | Msg.TransportConnection _ := "TransportConnectionMsg"
        | Msg.PubSubTopic _ := "PubSubTopicMsg"
        | Msg.Storage _ := "StorageMsg"
        | Msg.Ticker _ := "TickerMsg"
        | Msg.Template _ := "TemplateMsg"
        | Msg.TemplateMinimum _ := "TemplateMinimumMsg"
      };
    
    -- Helper to convert a single message to its Mermaid string representation
    messageToMermaid (message : EngineMsg Msg) : String :=
      let
        senderStr : String := engineIdToString (EngineMsg.sender message);
        targetStr : String := engineIdToString (EngineMsg.target message);
        label : String := msgToString (EngineMsg.msg message);
      in "    " ++str senderStr ++str "->>" ++str targetStr ++str ": " ++str label ++str "\n";
    
    -- Function to pretty print the message list as a Mermaid sequence diagram
    prettyPrintMessageList (messages : List (EngineMsg Msg)) : String :=
      let
        participantsSet : Set String := getParticipants messages;
        participantDeclarations : String := stringJoin "\n    " (map (\{p := "participant " ++str p}) (Set.toList participantsSet));
        
        messageLines : String := stringJoin "" (map messageToMermaid messages);
    
      in "sequenceDiagram\n"
         ++str "    autonumber\n"
         ++str (if | Set.isEmpty participantsSet := "" | else := "    " ++str participantDeclarations ++str "\n")
         ++str messageLines;
    ``` 
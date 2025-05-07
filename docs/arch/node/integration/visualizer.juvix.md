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
    import arch.node.types.transport open; -- For TransportAddress etc.

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
    import tutorial.engines.template_minimum_messages as TemplateMinimum;
    
    -- Function to convert EngineID to a String for diagram labels
    engineIdToString (eid : EngineID) : String :=
      let
        nodeStr := case fst eid of {
          | none := "Client" -- Or some other placeholder for external senders
          | some (PublicKey.Curve25519PubKey pk) := pk
        };
        engineNameStr := snd eid;
      in nodeStr ++str "/" ++str engineNameStr;
    
    -- Helper function to convert NodeID to a String
    nodeIdToString (nodeId : NodeID) : String :=
      case nodeId of {
        | PublicKey.Curve25519PubKey pk := pk
      };
    
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
    
    -- Placeholder for Hash to String conversion
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
    
    -- Placeholders for complex types
    signableToString (s : Signable) : String := "<Signable>";
    commitmentToString (c : Commitment) : String := "<Commitment>";
    ciphertextToString (c : Ciphertext) : String := "<Ciphertext>";
    plaintextToString (p : Plaintext) : String := "<Plaintext>";
    readsForEvidenceToString (rfe : ReadsForEvidence) : String := "<ReadsForEvidence>";
    signsForEvidenceToString (sfe : SignsForEvidence) : String := "<SignsForEvidence>";
    backendToString (b : Backend) : String := "<Backend>";
    idParamsToString (p : IDParams) : String := "<IDParams>";
    capabilitiesToString (c : Capabilities) : String := "<Capabilities>";
    routerMsgInnerToString (r : RouterMsg Msg) : String := "<RouterMsgInner>";
    transportAddressToString (t : TransportAddress) : String := "<TransportAddress>";
    byteStringToString (b : ByteString) : String := "<ByteString>";
    chunkIdToString (c : ChunkID) : String := "<ChunkID>";
    topicIdToString (t : TopicID) : String := "<TopicID>";
    epochTimestampToString (et : Nat) : String := natToString et;
    tsStorageDBQueryToString (q : TSStorageDBQuery) : String := "<TSQuery>";
    tsStorageDBDataToString (d : TSStorageDBData) : String := "<TSData>";
    storageKeyToString (k : String) : String := k;
    storageValueToString (v : String) : String := v;
    encryptedMsgToString (em : EncryptedMsg) : String := "<EncryptedMsg>";
    
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
    
    -- Identity Management
    identityManagementMsgToString (imMsg : IdentityManagementMsg) : String :=
      case imMsg of {
        | IdentityManagementMsg.GenerateIdentityRequest req :=
          "GenerateIdReq(be:" ++str (backendToString (RequestGenerateIdentity.backend req)) ++str ",cap:" ++str (capabilitiesToString (RequestGenerateIdentity.capabilities req)) ++str ")"
        | IdentityManagementMsg.GenerateIdentityReply reply :=
          "GenerateIdReply(extId:" ++str (engineIdToString (ReplyGenerateIdentity.externalIdentity reply)) ++str ",err:" ++str (option (ReplyGenerateIdentity.err reply) "None" id) ++str ")"
        | IdentityManagementMsg.ConnectIdentityRequest req :=
          "ConnectIdReq(id:" ++str (engineIdToString (RequestConnectIdentity.externalIdentity req)) ++str ",be:" ++str (backendToString (RequestConnectIdentity.backend req)) ++str ")"
        | IdentityManagementMsg.ConnectIdentityReply reply :=
          "ConnectIdReply(err:" ++str (option (ReplyConnectIdentity.err reply) "None" id) ++str ")"
        | IdentityManagementMsg.DeleteIdentityRequest req :=
          "DeleteIdReq(id:" ++str (engineIdToString (RequestDeleteIdentity.externalIdentity req)) ++str ",be:" ++str (backendToString (RequestDeleteIdentity.backend req)) ++str ")"
        | IdentityManagementMsg.DeleteIdentityReply reply :=
          "DeleteIdReply(err:" ++str (option (ReplyDeleteIdentity.err reply) "None" id) ++str ")"
      };

    -- Decryption
    decryptionMsgToString (decMsg : DecryptionMsg) : String :=
      case decMsg of {
        | DecryptionMsg.Request req := "DecryptReq(data:" ++str (ciphertextToString (RequestDecryption.data req)) ++str ")"
        | DecryptionMsg.Reply reply := "DecryptReply(data:" ++str (plaintextToString (ReplyDecryption.data reply)) ++str ",err:" ++str (option (ReplyDecryption.err reply) "None" id) ++str ")"
      };

    -- Encryption
    encryptionMsgToString (encMsg : EncryptionMsg) : String :=
      case encMsg of {
        | EncryptionMsg.Request req := "EncryptReq(id:" ++str (externalIdentityToString (RequestEncrypt.externalIdentity req)) ++str ",readsFor:" ++str (boolToString (RequestEncrypt.useReadsFor req)) ++str ")"
        | EncryptionMsg.Reply reply := "EncryptReply(data:" ++str (ciphertextToString (ReplyEncrypt.ciphertext reply)) ++str ",err:" ++str (option (ReplyEncrypt.err reply) "None" id) ++str ")"
      };

    -- Commitment
    commitmentMsgToString (comMsg : CommitmentMsg) : String :=
      case comMsg of {
        | CommitmentMsg.Request req := "CommitReq(data:" ++str (signableToString (RequestCommitment.data req)) ++str ")"
        | CommitmentMsg.Reply reply := "CommitReply(commit:" ++str (commitmentToString (ReplyCommitment.commitment reply)) ++str ",err:" ++str (option (ReplyCommitment.err reply) "None" id) ++str ")"
      };

    -- Verification
    verificationMsgToString (verMsg : VerificationMsg) : String :=
      case verMsg of {
        | VerificationMsg.Request req :=
          "VerifyReq(id:" ++str (externalIdentityToString (RequestVerification.externalIdentity req)) ++str ",useSf:" ++str (boolToString (RequestVerification.useSignsFor req)) ++str ")" -- Removed vk, using actual fields
        | VerificationMsg.Reply reply :=
          "VerifyReply(ok:" ++str (boolToString (ReplyVerification.result reply)) ++str ",err:" ++str (option (ReplyVerification.err reply) "None" id) ++str ")"
      };

    -- ReadsFor
    readsForMsgToString (rfMsg : ReadsForMsg) : String :=
      case rfMsg of {
        | ReadsForMsg.Request req := "ReadsForReq(A:" ++str (externalIdentityToString (RequestReadsFor.externalIdentityA req)) ++str ",B:" ++str (externalIdentityToString (RequestReadsFor.externalIdentityB req)) ++str ")"
        | ReadsForMsg.Reply reply := "ReadsForReply(ok:" ++str (boolToString (ReplyReadsFor.readsFor reply)) ++str ",err:" ++str (option (ReplyReadsFor.err reply) "None" id) ++str ")"
        | ReadsForMsg.SubmitReadsForEvidenceRequest req := "SubmitReadsForEvReq(ev:" ++str (readsForEvidenceToString (RequestSubmitReadsForEvidence.evidence req)) ++str ")"
        | ReadsForMsg.SubmitReadsForEvidenceReply reply := "SubmitReadsForEvReply(err:" ++str (option (ReplySubmitReadsForEvidence.err reply) "None" id) ++str ")"
        | ReadsForMsg.QueryReadsForEvidenceRequest req := "QueryReadsForEvReq(id:" ++str (externalIdentityToString (RequestQueryReadsForEvidence.externalIdentity req)) ++str ")"
        | ReadsForMsg.QueryReadsForEvidenceReply reply := "QueryReadsForEvReply(id:" ++str (externalIdentityToString (ReplyQueryReadsForEvidence.externalIdentity reply)) ++str ",err:" ++str (option (ReplyQueryReadsForEvidence.err reply) "None" id) ++str ")"
      };

    -- SignsFor
    signsForMsgToString (sfMsg : SignsForMsg) : String :=
      case sfMsg of {
        | SignsForMsg.SignsForRequest req := "SignsForReq(A:" ++str (externalIdentityToString (RequestSignsFor.externalIdentityA req)) ++str ",B:" ++str (externalIdentityToString (RequestSignsFor.externalIdentityB req)) ++str ")"
        | SignsForMsg.SignsForReply reply := "SignsForReply(ok:" ++str (boolToString (ReplySignsFor.signsFor reply)) ++str ",err:" ++str (option (ReplySignsFor.err reply) "None" id) ++str ")"
        | SignsForMsg.SubmitSignsForEvidenceRequest req := "SubmitSignsForEvReq(ev:" ++str (signsForEvidenceToString (RequestSubmitSignsForEvidence.evidence req)) ++str ")"
        | SignsForMsg.SubmitSignsForEvidenceReply reply := "SubmitSignsForEvReply(err:" ++str (option (ReplySubmitSignsForEvidence.err reply) "None" id) ++str ")"
        | SignsForMsg.QuerySignsForEvidenceRequest req := "QuerySignsForEvReq(id:" ++str (externalIdentityToString (RequestQuerySignsForEvidence.externalIdentity req)) ++str ")"
        | SignsForMsg.QuerySignsForEvidenceReply reply := "QuerySignsForEvReply(id:" ++str (externalIdentityToString (ReplyQuerySignsForEvidence.externalIdentity reply)) ++str ",err:" ++str (option (ReplyQuerySignsForEvidence.err reply) "None" id) ++str ")"
      };
    
    -- Main dispatcher function for Msg to String
    terminating
    msgToString (actualMsg : Msg) : String :=
      case actualMsg of {
        | Msg.MempoolWorker mwMsg := mempoolWorkerMsgToString mwMsg
        | Msg.Shard shardMsg := shardMsgToString shardMsg
        | Msg.Executor execMsg := executorMsgToString execMsg
        | Msg.IdentityManagement imMsg := identityManagementMsgToString imMsg
        | Msg.Decryption decMsg := decryptionMsgToString decMsg
        | Msg.Encryption encMsg := encryptionMsgToString encMsg
        | Msg.Commitment comMsg := commitmentMsgToString comMsg
        | Msg.Verification verMsg := verificationMsgToString verMsg
        | Msg.ReadsFor rfMsg := readsForMsgToString rfMsg
        | Msg.SignsFor sfMsg := signsForMsgToString sfMsg
        | Msg.Naming nMsg := namingMsgToString nMsg
        | Msg.LocalKVStorage kvMsg := localKVStorageMsgToString kvMsg
        | Msg.Logging logMsg := loggingMsgToString logMsg
        | Msg.WallClock wcMsg := wallClockMsgToString wcMsg
        | Msg.LocalTSStorage tsMsg := localTSStorageMsgToString tsMsg
        | Msg.Router rMsg := routerMsgToString rMsg
        | Msg.TransportProtocol tpMsg := transportProtocolMsgToString tpMsg
        | Msg.TransportConnection tcMsg := transportConnectionMsgToString tcMsg
        | Msg.PubSubTopic psMsg := pubSubTopicMsgToString psMsg
        | Msg.Storage stMsg := storageMsgToString stMsg
        | Msg.Ticker tMsg := tickerMsgToString tMsg
        | Msg.Template tMsg := templateMsgToString tMsg
        | Msg.TemplateMinimum tmMsg := templateMinimumMsgToString tmMsg
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

    -- Local Key Value Storage
    localKVStorageMsgToString (kvMsg : LocalKVStorageMsg) : String :=
      case kvMsg of {
        | LocalKVStorageMsg.GetValueRequest req := "KVGetReq(key:" ++str (storageKeyToString (GetValueKVStoreRequest.key req)) ++str ")"
        | LocalKVStorageMsg.GetValueReply reply := "KVGetReply(key:" ++str (storageKeyToString (GetValueKVStoreReply.key reply)) ++str ",val:" ++str (storageValueToString (GetValueKVStoreReply.value reply)) ++str ")"
        | LocalKVStorageMsg.SetValueRequest req := "KVSetReq(key:" ++str (storageKeyToString (SetValueKVStoreRequest.key req)) ++str ",val:" ++str (storageValueToString (SetValueKVStoreRequest.value req)) ++str ")"
        | LocalKVStorageMsg.SetValueReply reply := "KVSetReply(key:" ++str (storageKeyToString (SetValueKVStoreReply.key reply)) ++str ",ok:" ++str (boolToString (SetValueKVStoreReply.success reply)) ++str ")"
        | LocalKVStorageMsg.DeleteValueRequest req := "KVDelReq(key:" ++str (storageKeyToString (DeleteValueKVStoreRequest.key req)) ++str ")"
        | LocalKVStorageMsg.DeleteValueReply reply := "KVDelReply(key:" ++str (storageKeyToString (DeleteValueKVStoreReply.key reply)) ++str ",ok:" ++str (boolToString (DeleteValueKVStoreReply.success reply)) ++str ")"
        | LocalKVStorageMsg.ValueChanged notice := "KVChanged(key:" ++str (storageKeyToString (ValueChangedKVStore.key notice)) ++str ",val:" ++str (storageValueToString (ValueChangedKVStore.value notice)) ++str ",ts:" ++str (epochTimestampToString (ValueChangedKVStore.timestamp notice)) ++str ")"
      };

    -- Wall Clock
    wallClockMsgToString (wcMsg : WallClockMsg) : String :=
      case wcMsg of {
        | WallClockMsg.GetTime := "GetTimeReq"
        | WallClockMsg.GetTimeResult reply := "GetTimeReply(ts:" ++str (epochTimestampToString (TimeResult.epochTime reply)) ++str ")"
      };

    -- Local Time Series Storage
    localTSStorageMsgToString (tsMsg : LocalTSStorageMsg) : String :=
      case tsMsg of {
        | LocalTSStorageMsg.GetRequest req := "TSGetReq(q:" ++str (tsStorageDBQueryToString (GetDataTSStorageDBRequest.query req)) ++str ")"
        | LocalTSStorageMsg.GetReply reply := "TSGetReply(q:" ++str (tsStorageDBQueryToString (GetDataTSStorageDBReply.query reply)) ++str ",data:" ++str (tsStorageDBDataToString (GetDataTSStorageDBReply.data reply)) ++str ")"
        | LocalTSStorageMsg.RecordRequest req := "TSRecordReq(q:" ++str (tsStorageDBQueryToString (RecordDataTSStorageDBRequest.query req)) ++str ")"
        | LocalTSStorageMsg.RecordReply reply := "TSRecordReply(q:" ++str (tsStorageDBQueryToString (RecordDataTSStorageDBReply.query reply)) ++str ",ok:" ++str (boolToString (RecordDataTSStorageDBReply.success reply)) ++str ")"
        | LocalTSStorageMsg.DeleteRequest req := "TSDeleteReq(q:" ++str (tsStorageDBQueryToString (DeleteDataTSStorageDBRequest.query req)) ++str ")"
        | LocalTSStorageMsg.DeleteReply reply := "TSDeleteReply(q:" ++str (tsStorageDBQueryToString (DeleteDataTSStorageDBReply.query reply)) ++str ",ok:" ++str (boolToString (DeleteDataTSStorageDBReply.success reply)) ++str ")"
        | LocalTSStorageMsg.DataChanged notice := "TSDataChanged(q:" ++str (tsStorageDBQueryToString (DataChangedTSStorageDB.query notice)) ++str ",data:" ++str (tsStorageDBDataToString (DataChangedTSStorageDB.data notice)) ++str ",ts:" ++str (epochTimestampToString (DataChangedTSStorageDB.timestamp notice)) ++str ")"
      };

    -- Net Registry
    netRegistryMsgToString (nrMsg : NetworkRegistryMsg) : String :=
      case nrMsg of {
        | NetworkRegistryMsg.NodeAdvert advert := "NodeAdvert(id:" ++str (nodeIdToString (NodeAdvert.id advert)) ++str ",v:" ++str (natToString (NodeAdvert.version advert)) ++str ")"
        | NetworkRegistryMsg.TopicAdvert advert := "TopicAdvert(id:" ++str (topicIdToString (TopicAdvert.id advert)) ++str ",v:" ++str (natToString (TopicAdvert.version advert)) ++str ")"
        | NetworkRegistryMsg.GetNodeAdvertRequest req := "GetNodeAdvertReq(id:" ++str (nodeIdToString req) ++str ")"
        | NetworkRegistryMsg.GetNodeAdvertReply reply := "GetNodeAdvertReply(ok:" ++str (boolToString (isRight reply)) ++str ")" -- Simplified
        | NetworkRegistryMsg.GetTopicAdvertRequest req := "GetTopicAdvertReq(id:" ++str (topicIdToString req) ++str ")"
        | NetworkRegistryMsg.GetTopicAdvertReply reply := "GetTopicAdvertReply(ok:" ++str (boolToString (isRight reply)) ++str ")" -- Simplified
      };

    -- Router
    routerMsgToString (rMsg : RouterMsg Msg) : String :=
      case rMsg of {
        | RouterMsg.NodeAdvert advert := "NodeAdvert(id:" ++str (nodeIdToString (NodeAdvert.id advert)) ++str ")"
        | RouterMsg.Send outMsg := "RouterSend(to:" ++str (engineIdToString (EngineMsg.target (NodeOutMsg.msg outMsg))) ++str ")" -- Simplified
        | RouterMsg.Recv inMsg := "RouterRecv(seq:" ++str (natToString (NodeMsg.seq inMsg)) ++str ")"
        | RouterMsg.ConnectRequest req := "RouterConnectReq(src:" ++str (nodeIdToString (ConnectRequest.src_node_id req)) ++str ")"
        | RouterMsg.ConnectReply reply := "RouterConnectReply(ok:" ++str (boolToString (isRight reply)) ++str ")" -- Simplified
        | RouterMsg.SetPermanence perm := "SetPermanence(" ++str (case perm of { | ConnectionPermanence.RouterMsgConnectionEphemeral := "Eph" | ConnectionPermanence.RouterMsgConnectionPermanent := "Perm"}) ++str ")"
      };

    -- Transport Protocol
    transportProtocolMsgToString (tpMsg : TransportProtocolMsg) : String :=
      case tpMsg of {
        | TransportProtocolMsg.Send req := "TpSend(addr:" ++str (transportAddressToString (TransportOutMsg.addr req)) ++str ")"
      };

    -- Transport Connection
    transportConnectionMsgToString (tcMsg : TransportConnectionMsg) : String :=
      case tcMsg of {
        | TransportConnectionMsg.Send outMsg :=
          let
            innerNodeMsg := TransportConnectionOutMsg.msg outMsg;
            seqStr := natToString (NodeMsg.seq innerNodeMsg);
            encMsgDetailStr := encryptedMsgToString (NodeMsg.msg innerNodeMsg);
          in "TcSend(seq:" ++str seqStr ++str ", msg:" ++str encMsgDetailStr ++str ")"
      };

    -- Pub Sub Topic
    pubSubTopicMsgToString (psMsg : PubSubTopicMsg) : String :=
      case psMsg of {
        | PubSubTopicMsg.Forward _ := "PsForward" -- Placeholder for TopicMsg details
        | PubSubTopicMsg.SubRequest req := "PsSubReq(topic:" ++str (topicIdToString (TopicSubRequest.topic req)) ++str ")"
        | PubSubTopicMsg.SubReply reply := "PsSubReply(ok:" ++str (boolToString (isRight reply)) ++str ")"
        | PubSubTopicMsg.UnsubRequest req := "PsUnsubReq(topic:" ++str (topicIdToString (TopicUnsubRequest.topic req)) ++str ")"
        | PubSubTopicMsg.UnsubReply reply := "PsUnsubReply(ok:" ++str (boolToString (isRight reply)) ++str ")"
      };

    -- Storage
    storageMsgToString (stMsg : StorageMsg) : String :=
      case stMsg of {
        | StorageMsg.ChunkGetRequest req := "ChunkGetReq(id:" ++str (chunkIdToString (ChunkGetRequest.chunk req)) ++str ")"
        | StorageMsg.ChunkGetReply reply := "ChunkGetReply(ok:" ++str (boolToString (isRight reply)) ++str ")" -- Simplified
        | StorageMsg.ChunkPutRequest _ := "ChunkPutReq" -- Chunk type has no ID field
        | StorageMsg.ChunkPutReply reply := "ChunkPutReply(ok:" ++str (boolToString (isRight reply)) ++str ")" -- Simplified
      };

    -- Ticker
    tickerMsgToString (tMsg : TickerMsg) : String :=
      case tMsg of {
        | TickerMsg.Increment := "TickInc"
        | TickerMsg.CountRequest := "TickCountReq"
        | TickerMsg.CountReply reply := "TickCountReply(val:" ++str (natToString (CountReply.counter reply)) ++str ")"
      };

    -- Template
    templateMsgToString (tMsg : TemplateMsg) : String :=
      case tMsg of {
        | TemplateMsg.JustHi := "TemplateHi"
        | TemplateMsg.ExampleRequest (ExampleRequest.mk@{argOne := a1; argTwo := a2}) := "TemplateExampleReq(a1:" ++str (natToString a1) ++str ",a2:" ++str (natToString a2) ++str ")"
        | TemplateMsg.ExampleReply reply := "TemplateExampleReply(ok:" ++str (boolToString (isRight reply)) ++str ")" -- Simplified
      };

    -- TemplateMinimum
    templateMinimumMsgToString (tmMsg : TemplateMinimum.TemplateMinimumMsg) : String :=
      case tmMsg of {
        | TemplateMinimum.TemplateMinimumMsg.JustHi := "TemplateMinimumHi"
        | TemplateMinimum.TemplateMinimumMsg.ExampleRequest req :=
          "TemplateMinExampleReq(a1:" ++str (natToString (TemplateMinimum.ExampleRequest.argOne req)) ++str ",a2:" ++str (natToString (TemplateMinimum.ExampleRequest.argTwo req)) ++str ")"
        | TemplateMinimum.TemplateMinimumMsg.ExampleReply reply :=
          case reply of {
            | right payload := "TemplateMinExampleReply(ok:" ++str (TemplateMinimum.ReplyPayload.payload payload) ++str ")"
            | left err := "TemplateMinExampleReply(err:" ++str (TemplateMinimum.ReplyError.error err) ++str ")"
          }
      };
    ``` 
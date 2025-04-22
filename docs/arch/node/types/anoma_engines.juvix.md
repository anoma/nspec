<!-- --8<-- [start:Eng] -->
```juvix
module arch.node.types.anoma_engines;

import prelude open;
import arch.node.types.anoma_message open;
import arch.node.types.anoma_config open;
import arch.node.types.anoma_environment open;
import arch.node.types.engine open;
import arch.node.types.identities open;
import arch.node.types.messages open;
import arch.node.types.engine_behaviour open;
import arch.node.types.router open;
import arch.node.engines.router_config open;
import arch.node.engines.router_environment open;
import arch.node.engines.transport_protocol_config open;
import arch.node.engines.transport_protocol_environment open;
import arch.node.engines.transport_connection_config open;
import arch.node.engines.transport_connection_environment open;
import arch.node.engines.pub_sub_topic_config open;
import arch.node.engines.pub_sub_topic_environment open;
import arch.node.engines.storage_config open;
import arch.node.engines.storage_environment open;

{- Identity -}
import arch.node.engines.identity_management open;
import arch.node.engines.decryption open;
import arch.node.engines.encryption open;
import arch.node.engines.commitment open;
import arch.node.engines.verification open;
import arch.node.engines.reads_for open;
import arch.node.engines.signs_for open;
import arch.node.engines.naming open;

{- Hardware -}
import arch.node.engines.local_key_value_storage open;
import arch.node.engines.logging open;
import arch.node.engines.wall_clock open;
import arch.node.engines.local_time_series_storage open;

{- Network -}
import arch.node.engines.router open;
import arch.node.engines.transport_protocol open;
import arch.node.engines.transport_connection open;
import arch.node.engines.pub_sub_topic open;
import arch.node.engines.storage open;

{- Ordering -}
import arch.node.engines.mempool_worker open;
import arch.node.engines.executor open;
import arch.node.engines.shard open;

{- Misc -}
import arch.node.engines.ticker open;

{- Templates -}
import tutorial.engines.template open;
import tutorial.engines.template_minimum open;

import arch.node.types.crypto open;

type Eng :=
  {- Identity -}
  | EngIdentityManagement IdentityManagementEngine
  | EngDecryption DecryptionEngine
  | EngEncryption EncryptionEngine
  | EngCommitment CommitmentEngine
  | EngVerification VerificationEngine
  | EngReadsFor ReadsForEngine
  | EngSignsFor SignsForEngine
  | EngNaming NamingEngine

  {- Hardware -}
  | EngLocalKeyValueStorage LocalKVStorageEngine
  | EngLogging LoggingEngine
  | EngWallClock WallClockEngine
  | EngLocalTSeries LocalTSStorageEngine

  {- Network -}
  | EngRouter RouterEngine
  | EngTransportProtocol TransportProtocolEngine
  | EngTransportConnection TransportConnectionEngine
  | EngPubSubTopic PubSubTopicEngine
  | EngStorage StorageEngine

  {- Ordering -}
  | EngMempoolWorker (MempoolWorkerEngine String String ByteString String)
  | EngExecutor (ExecutorEngine String String ByteString String)
  | EngShard (ShardEngine String String ByteString String)

  {- Misc -}
  | EngTicker TickerEngine

  {- Templates -}
  | EngTemplate TemplateEngine
  | EngTemplateMinimum TemplateMinimumEngine
  ;
```

```juvix
mkEng (nodeId : NodeID) (p : Pair Cfg Env) : Option (Pair Eng EngineID) :=
  case p of {
  | mkPair (CfgIdentityManagement cfg) (EnvIdentityManagement env) :=
    let
      eng := EngIdentityManagement (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := identityManagementBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgDecryption cfg) (EnvDecryption env) :=
    let
      eng := EngDecryption (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := decryptionBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgEncryption cfg) (EnvEncryption env) :=
    let
      eng := EngEncryption (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := encryptionBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgCommitment cfg) (EnvCommitment env) :=
    let
      eng := EngCommitment (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := commitmentBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgVerification cfg) (EnvVerification env) :=
    let
      eng := EngVerification (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := verificationBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgReadsFor cfg) (EnvReadsFor env) :=
    let
      eng := EngReadsFor (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := readsForBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgSignsFor cfg) (EnvSignsFor env) :=
    let
      eng := EngSignsFor (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := signsForBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgNaming cfg) (EnvNaming env) :=
    let
      eng := EngNaming (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := namingBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgLocalKeyValueStorage cfg) (EnvLocalKeyValueStorage env) :=
    let
      eng := EngLocalKeyValueStorage (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := localKVStorageBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgLogging cfg) (EnvLogging env) :=
    let
      eng := EngLogging (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := loggingBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgWallClock cfg) (EnvWallClock env) :=
    let
      eng := EngWallClock (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := wallClockBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgLocalTSeries cfg) (EnvLocalTSeries env) :=
    let
      eng := EngLocalTSeries (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := localTSStorageBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgRouter cfg) (EnvRouter env) :=
    let
      eng := EngRouter (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgTransportProtocol cfg) (EnvTransportProtocol env) :=
    let
      eng := EngTransportProtocol (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgTransportConnection cfg) (EnvTransportConnection env) :=
    let
      eng := EngTransportConnection (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgPubSubTopic cfg) (EnvPubSubTopic env) :=
    let
      eng := EngPubSubTopic (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgStorage cfg) (EnvStorage env) :=
    let
      eng := EngStorage (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgMempoolWorker cfg) (EnvMempoolWorker env) :=
    let
      eng := EngMempoolWorker (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := mempoolWorkerBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgExecutor cfg) (EnvExecutor env) :=
    let
      eng := EngExecutor (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := executorBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgShard cfg) (EnvShard env) :=
    let
      eng := EngShard (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := shardBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgTicker cfg) (EnvTicker env) :=
    let
      eng := EngTicker (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := tickerBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgTemplate cfg) (EnvTemplate env) :=
    let
      eng := EngTemplate (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (CfgTemplateMinimum cfg) (EnvTemplateMinimum env) :=
    let
      eng := EngTemplateMinimum (mkEngine@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | _ := none
  };
```
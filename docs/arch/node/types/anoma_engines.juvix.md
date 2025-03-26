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

mkEng (nodeId : NodeID) (nameMap : String -> String) (p : Pair Cfg Env) : Option (Pair Eng EngineName) :=
  case p of {
  | mkPair (CfgIdentityManagement cfg) (EnvIdentityManagement env) :=
    let
      engineCfg : EngineCfg IdentityManagementCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "identity_management";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngIdentityManagement (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := identityManagementBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgDecryption cfg) (EnvDecryption env) :=
    let
      engineCfg : EngineCfg DecryptionCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "decryption";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngDecryption (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := decryptionBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgEncryption cfg) (EnvEncryption env) :=
    let
      engineCfg : EngineCfg EncryptionCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "encryption";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngEncryption (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := encryptionBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgCommitment cfg) (EnvCommitment env) :=
    let
      engineCfg : EngineCfg CommitmentCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "commitment";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngCommitment (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := commitmentBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgVerification cfg) (EnvVerification env) :=
    let
      engineCfg : EngineCfg VerificationCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "verification";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngVerification (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := verificationBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgReadsFor cfg) (EnvReadsFor env) :=
    let
      engineCfg : EngineCfg ReadsForCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "reads_for";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngReadsFor (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := readsForBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgSignsFor cfg) (EnvSignsFor env) :=
    let
      engineCfg : EngineCfg SignsForCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "signs_for";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngSignsFor (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := signsForBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgNaming cfg) (EnvNaming env) :=
    let
      engineCfg : EngineCfg NamingCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "naming";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngNaming (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := namingBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgLocalKeyValueStorage cfg) (EnvLocalKeyValueStorage env) :=
    let
      engineCfg : EngineCfg LocalKVStorageCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "local_key_value_storage";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngLocalKeyValueStorage (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := localKVStorageBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgLogging cfg) (EnvLogging env) :=
    let
      engineCfg : EngineCfg LoggingCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "logging";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngLogging (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := loggingBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgWallClock cfg) (EnvWallClock env) :=
    let
      engineCfg : EngineCfg WallClockCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "wall_clock";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngWallClock (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := wallClockBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgLocalTSeries cfg) (EnvLocalTSeries env) :=
    let
      engineCfg : EngineCfg LocalTSStorageCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "local_time_series_storage";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngLocalTSeries (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := localTSStorageBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgRouter cfg) (EnvRouter env) :=
    let
      engineCfg : EngineCfg RouterLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngRouter (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | mkPair (CfgTransportProtocol cfg) (EnvTransportProtocol env) :=
    let
      engineCfg : EngineCfg TransportProtocolLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngTransportProtocol (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | mkPair (CfgTransportConnection cfg) (EnvTransportConnection env) :=
    let
      engineCfg : EngineCfg TransportConnectionLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngTransportConnection (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | mkPair (CfgPubSubTopic cfg) (EnvPubSubTopic env) :=
    let
      engineCfg : EngineCfg PubSubTopicLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngPubSubTopic (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | mkPair (CfgStorage cfg) (EnvStorage env) :=
    let
      engineCfg : EngineCfg StorageLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngStorage (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | mkPair (CfgMempoolWorker cfg) (EnvMempoolWorker env) :=
    let
      engineCfg : EngineCfg (MempoolWorkerCfg String) :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "mempool_worker";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngMempoolWorker (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := mempoolWorkerBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgExecutor cfg) (EnvExecutor env) :=
    let
      engineCfg : EngineCfg (ExecutorCfg String ByteString) :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "executor";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngExecutor (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := executorBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgShard cfg) (EnvShard env) :=
    let
      engineCfg : EngineCfg ShardCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "shard";
          cfg := cfg;
        };
      name := EngineCfg.name engineCfg;
      eng := EngShard (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := shardBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgTicker cfg) (EnvTicker env) :=
    let
      engineCfg : EngineCfg TickerLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngTicker (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := tickerBehaviour;
      });
    in some (mkPair eng name)
  | mkPair (CfgTemplate cfg) (EnvTemplate env) :=
    let
      engineCfg : EngineCfg TemplateLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngTemplate (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | mkPair (CfgTemplateMinimum cfg) (EnvTemplateMinimum env) :=
    let
      engineCfg : EngineCfg TemplateMinimumLocalCfg :=
        TODO;
      name := EngineCfg.name engineCfg;
      eng := EngTemplateMinimum (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      });
    in some (mkPair eng name)
  | _ := none
  };
```
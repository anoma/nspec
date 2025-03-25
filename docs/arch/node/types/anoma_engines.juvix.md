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

mkEng (nodeId : NodeID) (nameMap : String -> String) (p : Pair Cfg Env) : Option Eng :=
  case p of {
  | mkPair (CfgIdentityManagement cfg) (EnvIdentityManagement env) :=
    let
      engineCfg : EngineCfg IdentityManagementCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "identity_management";
          cfg := cfg;
        };
    in
      some (EngIdentityManagement (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := identityManagementBehaviour;
      }))
  | mkPair (CfgDecryption cfg) (EnvDecryption env) :=
    let
      engineCfg : EngineCfg DecryptionCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "decryption";
          cfg := cfg;
        };
    in
      some (EngDecryption (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := decryptionBehaviour;
      }))
  | mkPair (CfgEncryption cfg) (EnvEncryption env) :=
    let
      engineCfg : EngineCfg EncryptionCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "encryption";
          cfg := cfg;
        };
    in
      some (EngEncryption (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := encryptionBehaviour;
      }))
  | mkPair (CfgCommitment cfg) (EnvCommitment env) :=
    let
      engineCfg : EngineCfg CommitmentCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "commitment";
          cfg := cfg;
        };
    in
      some (EngCommitment (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := commitmentBehaviour;
      }))
  | mkPair (CfgVerification cfg) (EnvVerification env) :=
    let
      engineCfg : EngineCfg VerificationCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "verification";
          cfg := cfg;
        };
    in
      some (EngVerification (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := verificationBehaviour;
      }))
  | mkPair (CfgReadsFor cfg) (EnvReadsFor env) :=
    let
      engineCfg : EngineCfg ReadsForCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "reads_for";
          cfg := cfg;
        };
    in
      some (EngReadsFor (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := readsForBehaviour;
      }))
  | mkPair (CfgSignsFor cfg) (EnvSignsFor env) :=
    let
      engineCfg : EngineCfg SignsForCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "signs_for";
          cfg := cfg;
        };
    in
      some (EngSignsFor (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := signsForBehaviour;
      }))
  | mkPair (CfgNaming cfg) (EnvNaming env) :=
    let
      engineCfg : EngineCfg NamingCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "naming";
          cfg := cfg;
        };
    in
      some (EngNaming (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := namingBehaviour;
      }))
  | mkPair (CfgLocalKeyValueStorage cfg) (EnvLocalKeyValueStorage env) :=
    let
      engineCfg : EngineCfg LocalKVStorageCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "local_key_value_storage";
          cfg := cfg;
        };
    in
      some (EngLocalKeyValueStorage (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := localKVStorageBehaviour;
      }))
  | mkPair (CfgLogging cfg) (EnvLogging env) :=
    let
      engineCfg : EngineCfg LoggingCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "logging";
          cfg := cfg;
        };
    in
      some (EngLogging (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := loggingBehaviour;
      }))
  | mkPair (CfgWallClock cfg) (EnvWallClock env) :=
    let
      engineCfg : EngineCfg WallClockCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "wall_clock";
          cfg := cfg;
        };
    in
      some (EngWallClock (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := wallClockBehaviour;
      }))
  | mkPair (CfgLocalTSeries cfg) (EnvLocalTSeries env) :=
    let
      engineCfg : EngineCfg LocalTSStorageCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "local_time_series_storage";
          cfg := cfg;
        };
    in
      some (EngLocalTSeries (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := localTSStorageBehaviour;
      }))
  | mkPair (CfgRouter cfg) (EnvRouter env) :=
    let
      engineCfg : EngineCfg RouterLocalCfg :=
        TODO;
    in
      some (EngRouter (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | mkPair (CfgTransportProtocol cfg) (EnvTransportProtocol env) :=
    let
      engineCfg : EngineCfg TransportProtocolLocalCfg :=
        TODO;
    in
      some (EngTransportProtocol (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | mkPair (CfgTransportConnection cfg) (EnvTransportConnection env) :=
    let
      engineCfg : EngineCfg TransportConnectionLocalCfg :=
        TODO;
    in
      some (EngTransportConnection (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | mkPair (CfgPubSubTopic cfg) (EnvPubSubTopic env) :=
    let
      engineCfg : EngineCfg PubSubTopicLocalCfg :=
        TODO;
    in
      some (EngPubSubTopic (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | mkPair (CfgStorage cfg) (EnvStorage env) :=
    let
      engineCfg : EngineCfg StorageLocalCfg :=
        TODO;
    in
      some (EngStorage (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | mkPair (CfgMempoolWorker cfg) (EnvMempoolWorker env) :=
    let
      engineCfg : EngineCfg (MempoolWorkerCfg String) :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "mempool_worker";
          cfg := cfg;
        };
    in
      some (EngMempoolWorker (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := mempoolWorkerBehaviour;
      }))
  | mkPair (CfgExecutor cfg) (EnvExecutor env) :=
    let
      engineCfg : EngineCfg (ExecutorCfg String ByteString) :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "executor";
          cfg := cfg;
        };
    in
      some (EngExecutor (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := executorBehaviour;
      }))
  | mkPair (CfgShard cfg) (EnvShard env) :=
    let
      engineCfg : EngineCfg ShardCfg :=
        mkEngineCfg@{
          node := nodeId;
          name := nameMap "shard";
          cfg := cfg;
        };
    in
      some (EngShard (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := shardBehaviour;
      }))
  | mkPair (CfgTicker cfg) (EnvTicker env) :=
    let
      engineCfg : EngineCfg TickerLocalCfg :=
        TODO;
    in
      some (EngTicker (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := tickerBehaviour;
      }))
  | mkPair (CfgTemplate cfg) (EnvTemplate env) :=
    let
      engineCfg : EngineCfg TemplateLocalCfg :=
        TODO;
    in
      some (EngTemplate (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | mkPair (CfgTemplateMinimum cfg) (EnvTemplateMinimum env) :=
    let
      engineCfg : EngineCfg TemplateMinimumLocalCfg :=
        TODO;
    in
      some (EngTemplateMinimum (mkEngine@{
        cfg := engineCfg;
        env := env;
        behaviour := TODO;
      }))
  | _ := none
  };
```
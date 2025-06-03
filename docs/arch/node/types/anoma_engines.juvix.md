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
import arch.system.state.resource_machine.notes.nockma open;

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
  | IdentityManagement IdentityManagementEngine
  | Decryption DecryptionEngine
  | Encryption EncryptionEngine
  | Commitment CommitmentEngine
  | Verification VerificationEngine
  | ReadsFor ReadsForEngine
  | SignsFor SignsForEngine
  | Naming NamingEngine

  {- Hardware -}
  | LocalKeyValueStorage LocalKVStorageEngine
  | Logging LoggingEngine
  | WallClock WallClockEngine
  | LocalTSeries LocalTSStorageEngine

  {- Network -}
  | Router RouterEngine
  | TransportProtocol TransportProtocolEngine
  | TransportConnection TransportConnectionEngine
  | PubSubTopic PubSubTopicEngine
  | Storage StorageEngine

  {- Ordering -}
  | MempoolWorker MempoolWorkerEngine
  | Executor ExecutorEngine
  | Shard ShardEngine

  {- Misc -}
  | Ticker TickerEngine

  {- Templates -}
  | Template TemplateEngine
  | TemplateMinimum TemplateMinimumEngine
  ;
```

```juvix
mkEng (nodeId : NodeID) (p : Pair Cfg Env) : Option (Pair Eng EngineID) :=
  case p of {
  | mkPair (Cfg.CfgIdentityManagement cfg) (Env.EnvIdentityManagement env) :=
    let
      eng := Eng.IdentityManagement (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := identityManagementBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgDecryption cfg) (Env.EnvDecryption env) :=
    let
      eng := Eng.Decryption (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := decryptionBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgEncryption cfg) (Env.EnvEncryption env) :=
    let
      eng := Eng.Encryption (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := encryptionBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgCommitment cfg) (Env.EnvCommitment env) :=
    let
      eng := Eng.Commitment (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := commitmentBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgVerification cfg) (Env.EnvVerification env) :=
    let
      eng := Eng.Verification (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := verificationBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgReadsFor cfg) (Env.EnvReadsFor env) :=
    let
      eng := Eng.ReadsFor (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := readsForBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgSignsFor cfg) (Env.EnvSignsFor env) :=
    let
      eng := Eng.SignsFor (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := signsForBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgNaming cfg) (Env.EnvNaming env) :=
    let
      eng := Eng.Naming (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := namingBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgLocalKeyValueStorage cfg) (Env.EnvLocalKeyValueStorage env) :=
    let
      eng := Eng.LocalKeyValueStorage (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := localKVStorageBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgLogging cfg) (Env.EnvLogging env) :=
    let
      eng := Eng.Logging (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := loggingBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgWallClock cfg) (Env.EnvWallClock env) :=
    let
      eng := Eng.WallClock (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := wallClockBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgLocalTSeries cfg) (Env.EnvLocalTSeries env) :=
    let
      eng := Eng.LocalTSeries (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := localTSStorageBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgRouter cfg) (Env.EnvRouter env) :=
    let
      eng := Eng.Router (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgTransportProtocol cfg) (Env.EnvTransportProtocol env) :=
    let
      eng := Eng.TransportProtocol (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgTransportConnection cfg) (Env.EnvTransportConnection env) :=
    let
      eng := Eng.TransportConnection (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgPubSubTopic cfg) (Env.EnvPubSubTopic env) :=
    let
      eng := Eng.PubSubTopic (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgStorage cfg) (Env.EnvStorage env) :=
    let
      eng := Eng.Storage (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgMempoolWorker cfg) (Env.EnvMempoolWorker env) :=
    let
      eng := Eng.MempoolWorker (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := mempoolWorkerBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgExecutor cfg) (Env.EnvExecutor env) :=
    let
      eng := Eng.Executor (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := executorBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgShard cfg) (Env.EnvShard env) :=
    let
      eng := Eng.Shard (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := shardBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgTicker cfg) (Env.EnvTicker env) :=
    let
      eng := Eng.Ticker (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := tickerBehaviour;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgTemplate cfg) (Env.EnvTemplate env) :=
    let
      eng := Eng.Template (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | mkPair (Cfg.CfgTemplateMinimum cfg) (Env.EnvTemplateMinimum env) :=
    let
      eng := Eng.TemplateMinimum (Engine.mk@{
        cfg := cfg@EngineCfg{node := nodeId};
        env := env;
        behaviour := TODO;
      });
      engineId := mkPair (some nodeId) (EngineCfg.name cfg);
    in some (mkPair eng engineId)
  | _ := none
  };
```

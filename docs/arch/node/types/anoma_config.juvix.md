---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_config;

    {- Identity -}

    import arch.node.engines.identity_management_config open;
    import arch.node.engines.decryption_config open;
    import arch.node.engines.encryption_config open;
    import arch.node.engines.commitment_config open;

    import arch.node.engines.verification_config open;
    import arch.node.engines.reads_for_config open;
    import arch.node.engines.signs_for_config open;
    import arch.node.engines.naming_config open;

    import arch.node.engines.local_key_value_storage_config open;
    import arch.node.engines.logging_config open;
    import arch.node.engines.wall_clock_config open;
    import arch.node.engines.local_time_series_storage_config open;

    {- Network -}

    import arch.node.engines.net_registry_config open;
    import arch.node.engines.router_config open;
    import arch.node.engines.transport_protocol_config open;
    import arch.node.engines.transport_connection_config open;
    import arch.node.engines.pub_sub_topic_config open;
    import arch.node.engines.storage_config open;

    {- Ordering -}

    import arch.node.engines.mempool_worker_config open;
    import arch.node.engines.executor_config open;
    import arch.node.engines.shard_config open;

    {- Misc -}

    import arch.node.engines.ticker_config open;

    {- Templates -}

    import tutorial.engines.template_config open;
    import tutorial.engines.template_minimum_config open;

    -- Add imports here
    ```

# Anoma Engine Configuration

An _Anoma_ engine configuration contains static, read-only configuration for an
engine. See [[Engine Configuration]] for more information.

Below is the definition of the type `Config`, which represents an Anoma engine
configuration. This means that each Anoma engine instance has a constant
configuration of type `Config`, initialised at creation.

For example, a configuration for an engine instance of the engine `TickerEngine`
is of type `TickerCfg`.

<!-- --8<-- [start:anoma-config-type] -->
```juvix
type Cfg :=

  {- Identity -}

  | CfgIdentityManagement IdentityManagementCfg
  | CfgDecryption DecryptionCfg
  | CfgEncryption EncryptionCfg
  | CfgCommitment CommitmentCfg

  | CfgVerification VerificationCfg
  | CfgReadsFor ReadsForCfg
  | CfgSignsFor SignsForCfg
  | CfgNaming NamingCfg

  {- Hardware -}

  | CfgLocalKeyValueStorage LocalKVStorageCfg
  | CfgLogging LoggingCfg
  | CfgWallClock WallClockCfg
  | CfgLocalTSeries LocalTSStorageCfg

  {- Network -}

  | CfgRouter RouterCfg
  -- | CfgNodeProxy NodeProxyCfg -- TODO: Add this back in
  | CfgTransportProtocol TransportProtocolCfg
  | CfgTransportConnection TransportConnectionCfg
  | CfgPubSubTopic PubSubTopicCfg
  | CfgStorage StorageCfg

  {- Ordering -}

  | CfgMempoolWorker MempoolWorkerCfg
  | CfgExecutor ExecutorCfg
  | CfgShard ShardCfg

  {- Misc -}

  | CfgTicker TickerCfg

  {- Templates -}

  | CfgTemplate TemplateCfg
  | CfgTemplateMinimum TemplateMinimumCfg

  -- Add more configurations here
```
<!-- --8<-- [end:anoma-config-type] -->

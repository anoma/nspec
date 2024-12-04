---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_config;

    {- Examples -}

    import arch.node.engines.template_config open;
    import arch.node.engines.ticker_config open;

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

    -- import arch.node.net.router_config open;
    -- import arch.node.net.node_proxy_config open;
    -- import arch.node.net.transport_config open;
    -- import arch.node.net.topic_config open;
    -- import arch.node.net.storage_config open;
    ```

# Anoma Engine Configuration

An _Anoma_ engine configuration contains static, read-only configuration for an engine.
See [[Engine Configuration]] for more information.

Below is the definition of the type `Config`,
which represents an Anoma engine configuration.
This means that each Anoma engine instance has a constant configuration of type `Config`, initialised at creation.

For example, a configuration for an engine instance
of the engine `TickerEngine` is of type `TickerCfg`.

<!-- --8<-- [start:anoma-config-type] -->
```juvix
type Cfg :=
  {- Examples -}

  | CfgTemplate TemplateCfg
  | CfgTicker TickerCfg

  {- Identity -}

  | CfgIdentityManagement IdentityManagementCfg
  | CfgDecryption DecryptionCfg
  | CfgEncryption EncryptionCfg
  | CfgCommitment CommitmentCfg

  | CfgVerification VerificationCfg
  | CfgReadsFor ReadsForCfg
  | CfgSignsFor SignsForCfg
  | CfgNaming NamingCfg

  | CfgLocalKeyValueStorage LocalKVStorageCfg
  | CfgLogging LoggingCfg
  | CfgWallClock WallClockCfg
  | CfgLocalTSeries LocalTSStorageCfg

  {- Network -}

  -- | CfgRouter RouterCfg
  -- | CfgNodeProxy NodeProxyCfg
  -- | CfgTransport TransportCfg
  -- | CfgTopic TopicCfg
  -- | CfgStorage StorageCfg
```
<!-- --8<-- [end:anoma-config-type] -->

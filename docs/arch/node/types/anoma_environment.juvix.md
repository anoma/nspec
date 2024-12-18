---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_environment;

    {- Examples -}

    import arch.node.engines.template_environment open;
    import arch.node.engines.ticker_environment open;

    {- Identity -}

    import arch.node.engines.identity_management_environment open;
    import arch.node.engines.decryption_environment open;
    import arch.node.engines.encryption_environment open;
    import arch.node.engines.commitment_environment open;

    import arch.node.engines.verification_environment open;
    import arch.node.engines.reads_for_environment open;
    import arch.node.engines.signs_for_environment open;
    import arch.node.engines.naming_environment open;

    import arch.node.engines.local_key_value_storage_environment open;
    import arch.node.engines.logging_environment open;
    import arch.node.engines.wall_clock_environment open;
    import arch.node.engines.local_time_series_storage_environment open;

    {- Network -}

    import arch.node.net.registry_environment open;
    import arch.node.net.router_environment open;
    import arch.node.net.transport_protocol_environment open;
    import arch.node.net.transport_connection_environment open;
    import arch.node.net.pub_sub_topic_environment open;
    import arch.node.net.storage_environment open;

    {- Ordering -}

    import arch.node.engines.mempool_worker_environment open;
    import arch.node.engines.executor_environment open;
    import arch.node.engines.shard_environment open;
    ```

# Anoma Engine Environments

An _Anoma_ engine environment is a collection of all the necessary
information/context that an engine instance needs to operate.
See [[Engine Environment]] for more information on engine environments.

Below is the definition of the type `Env`,
which represents an Anoma engine environment.
This means, an Anoma engine instance would have an environment of type `Env`.

For example, an environment for an engine instance
of the engine `TickerEngine` is of type `TickerEnvironment`.

<!-- --8<-- [start:anoma-environment-type] -->
```juvix
type Env :=
  {- Examples -}

  | EnvTemplate TemplateEnv
  | EnvTicker TickerEnv

  {- Identity -}

  | EnvIdentityManagement IdentityManagementEnv
  | EnvDecryption DecryptionEnv
  | EnvEncryption EncryptionEnv
  | EnvCommitment CommitmentEnv

  | EnvVerification VerificationEnv
  | EnvReadsFor ReadsForEnv
  | EnvSignsFor SignsForEnv
  | EnvNaming NamingEnv

  {- Hardware -}

  | EnvLocalKeyValueStorage LocalKVStorageEnv
  | EnvLogging LoggingEnv
  | EnvWallClock WallClockEnv
  | EnvLocalTSeries LocalTSStorageEnv

  {- Network -}

  | EnvNetworkRegistry NetworkRegistryEnv
  | EnvRouter RouterEnv
  | EnvPubSubTopic PubSubTopicEnv
  | EnvTransportProtocol TransportProtocolEnv
  | EnvTransportConnection TransportConnectionEnv
  | EnvStorage StorageEnv

  {- Ordering -}

  | EnvMempoolWorker MempoolWorkerEnv
  | EnvExecutor ExecutorEnv
  | EnvShard ShardEnv
```
<!-- --8<-- [end:anoma-environment-type] -->

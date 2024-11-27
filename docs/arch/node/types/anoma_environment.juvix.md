---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_environment;

    import arch.node.engines.template_environment open;
    import arch.node.engines.ticker_environment open;

--    import arch.node.engines.identity_management_environment open;
--    import arch.node.engines.decryption_environment open;
--    import arch.node.engines.encryption_environment open;
--    import arch.node.engines.commitment_environment open;
    import arch.node.engines.verification_environment open;
--    import arch.node.engines.reads_for_environment open;
    import arch.node.engines.signs_for_environment open;
--    import arch.node.engines.naming_environment open;
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
  | EnvTemplate TemplateEnv
  | EnvTicker TickerEnv

--  | EnvIdentityManagement IdentityManagementEnvironment
--  | EnvDecryption DecryptionEnvironment
--  | EnvEncryption EncryptionEnvironment
--  | EnvCommitment CommitmentEnvironment
  | EnvVerification VerificationEnv
--  | EnvReadsFor ReadsForEnvironment
  | EnvSignsFor SignsForEnv
--  | EnvNaming NamingEnvironment
```
<!-- --8<-- [end:anoma-environment-type] -->

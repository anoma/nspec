---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- naming-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.naming;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.naming_config open public;
    import arch.node.engines.naming_messages open public;
    import arch.node.engines.naming_environment open public;
    import arch.node.engines.naming_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open naming_config_example;
    open naming_environment_example;
    ```

# Naming Engine

The Naming Engine serves as the identity resolution system within Anoma, managing human-readable
names (`IdentityName`) and their associations with cryptographic identities (`ExternalIdentity`).
It can be compared to a decentralized DNS system that maintains verifiable connections between
user-friendly names and their corresponding cryptographic identities, while requiring evidence to
support these connections. The engine maintains an internal evidence store that tracks all verified
name-identity associations.

When users want to map names to identities, they interact with the engine in three main ways:

1. Name Resolution (`MsgNamingResolveNameRequest`): Users provide a human-readable name and receive
back any associated cryptographic identities (`ExternalIdentity`). This is like looking up who owns
a domain name, but with cryptographic verification.

2. Evidence Submission (`MsgNamingSubmitNameEvidenceRequest`): Users can submit evidence
(`IdentityNameEvidence`) that proves the connection between a name and an identity. The engine
verifies this evidence before storing it in its evidence store (`evidenceStore`). This is similar to
domain name registration, but requiring cryptographic proof of the right to associate a name with an
identity.

3. Evidence Querying (`MsgNamingQueryNameEvidenceRequest`): Users can look up all the evidence
associated with a particular cryptographic identity. This lets them verify the validity of
name-to-identity mappings and understand the history of name claims.

## Engine components

- [[Naming Messages]]
- [[Naming Configuration]]
- [[Naming Environment]]
- [[Naming Behaviour]]

## Type

<!-- --8<-- [start:NamingEngine] -->
```juvix
NamingEngine : Type :=
  Engine
    NamingCfg
    NamingLocalState
    NamingMailboxState
    NamingTimerHandle
    NamingActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:NamingEngine] -->

### Example of a naming engine

<!-- --8<-- [start:exampleNamingEngine] -->
```juvix
exampleNamingEngine : NamingEngine :=
  mkEngine@{
    cfg := namingCfg;
    env := namingEnv;
    behaviour := namingBehaviour;
  };
```
<!-- --8<-- [start:exampleNamingEngine] -->

where `namingCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_config.juvix.md:namingCfg"

where `namingEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_environment.juvix.md:namingEnv"

and `namingBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_behaviour.juvix.md:namingBehaviour"

---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity
  - engine
  - identity-management
  - engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.identity_management_messages open public;
    import arch.node.engines.identity_management_environment open public;
    import arch.node.engines.identity_management_behaviour open public;

    import arch.node.engines.identity_management_config open public;
    import arch.node.engines.identity_management_messages open public;
    import arch.node.engines.identity_management_environment open public;
    import arch.node.engines.identity_management_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open identity_management_config_example;
    open identity_management_environment_example;
    ```

# IdentityManagement Engine

---

The Identity Management Engine serves as the central coordinator for
identity operations within Anoma, managing the entire lifecycle of
identities across various storage systems (called "backends"). These backends
provide a service such as creating new identities, connecting to existing ones,
and managing their cryptographic capabilities (commiting and decrypting), while
abstracting away the complexity of different storage systems (e.g., local memory,
hardware devices, browser extensions, and remote machines).

---

Users can request new identity generation (via a
`MsgIdentityManagementGenerateIdentityRequest` message) or connection
to existing identities (via a
`MsgIdentityManagementConnectIdentityRequest` message), specifying
their desired capabilities. The Capabilities system in Anoma provides
fine-grained control over what operations an identity can perform. Each
identity can have commitment (signing) capabilities, decryption
capabilities, or both. When you create or connect to an identity, you
specify exactly which capabilities you need (via a term of the
`Capabilities` type), and the Identity Management Engine ensures you
only get access to those specific operations. `CapabilityCommit`
allows an identity to sign data - useful when you need to prove
authenticity or authorize actions but don't need to read encrypted
messages. `CapabilityDecrypt` enables decryption of messages intended
for that identity - essential when you need to receive encrypted
communications but don't need to sign anything.
`CapabilityCommitAndDecrypt` provides both abilities, letting an
identity both sign data and decrypt messages.

When connecting to an existing identity, you can request a subset of
that identity's capabilities but never more than it has. For example,
if an identity was created with only `CapabilityCommit`, you cannot
request decryption capabilities when connecting to it. The Identity
Management Engine enforces these restrictions and will return an error
if you request capabilities that are not available.

The Identity Management Engine handles the creation or connection process
and returns references to the appropriate [[Commitment]] and
[[Decryption]]  engines (via either a `ReplyGenerateIdentity` or
`MsgIdentityManagementConnectIdentityRequest` message) that provide
the requested capabilities. These engines are newly created in the
case of identity creation. Which engines are spawned are determined
by the requested capabilities.

Identity Management Engines maintain a registry of active identities
and their capabilities. When an identity is no longer needed, it can
be cleanly removed (via a `MsgIdentityManagementDeleteIdentityRequest`
message).

---

## Engine components

- [[Identity Management Messages]]
- [[Identity Management Configuration]]
- [[Identity Management Environment]]
- [[Identity Management Behaviour]]

---

## Type

<!-- --8<-- [start:IdentityManagementEngine] -->
```juvix
IdentityManagementEngine : Type :=
  Engine
    IdentityManagementCfg
    IdentityManagementLocalState
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:IdentityManagementEngine] -->

### Example of a identity management engine

<!-- --8<-- [start:exampleIdentityManagementEngine] -->
```juvix
exampleIdentityManagementEngine : IdentityManagementEngine :=
  mkEngine@{
    cfg := identityManagementCfg;
    env := identityManagementEnv;
    behaviour := identityManagementBehaviour;
  };
```
<!-- --8<-- [end:exampleIdentityManagementEngine] -->

where `identityManagementCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_config.juvix.md:identityManagementCfg"

`identityManagementEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_environment.juvix.md:identityManagementEnv"

and `identityManagementBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_behaviour.juvix.md:identityManagementBehaviour"

---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - identity-management
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management_environment;
    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.engine_environment open;
    import arch.node.engines.identity_management_messages open;
    import arch.node.types.anoma_message as Anoma open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
    ```

# Identity Management Environment

## Overview

The Identity Management Engine's environment maintains the state necessary for managing identities, including information about connected identities, backends, and capabilities.

??? code "Auxiliary Juvix code"

    ```juvix
    axiom genDecryptor : Backend -> Decryptor Backend Plaintext Ciphertext;
    axiom genSigner : Backend -> Signer Backend Signable Commitment
    ```

## Mailbox states

The Identity Management Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

### `IdentityManagementMailboxState`

```juvix
syntax alias IdentityManagementMailboxState := Unit;
```

## Local state

The local state of the Identity Management Engine includes information about the identities it manages.

### `IdentityInfo`

```juvix
type IdentityInfo := mkIdentityInfo@{
  backend : Backend;
  capabilities : Capabilities;
  commitmentEngine : Option EngineID;
  decryptionEngine : Option EngineID;
};
```

???+ code "Arguments"

    `backend`:
    : The backend associated with this identity.

    `capabilities`:
    : The capabilities available to this identity.

    `commitmentEngine`:
    : Optional reference to the commitment engine for this identity.

    `decryptionEngine`:
    : Optional reference to the decryption engine for this identity.

### `IdentityManagementLocalState`

```juvix
type IdentityManagementLocalState := mkIdentityManagementLocalState {
  identities : Map EngineID IdentityInfo;
};
```

???+ code "Arguments"

    `identities`:
    : Map of engine IDs to their corresponding identity information.

## Timer Handle

The Identity Management Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

### `IdentityManagementTimerHandle`

```juvix
syntax alias IdentityManagementTimerHandle := Unit;
```

## The Identity Management Environment

### `IdentityManagementEnv`

```juvix
IdentityManagementEnv : Type :=
  EngineEnv
    IdentityManagementLocalState
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:identityManagementEnv] -->
```juvix extract-module-statements
module identity_management_environment_example;

identityManagementEnv : IdentityManagementEnv :=
    mkEngineEnv@{
      localState := mkIdentityManagementLocalState@{
        identities := Map.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:identityManagementEnv] -->
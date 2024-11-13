---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- identity_management
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management_environment;
    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.engine_environment open;
    import arch.node.engines.identity_management_messages open;

    import arch.system.identity.identity open hiding {ExternalIdentity};
    ```

# Identity Management Environment

## Overview

The Identity Management Engine's environment maintains the state necessary for managing identities, including information about connected identities, backends, and capabilities.

## Mailbox states

The Identity Management Engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias IdentityManagementMailboxState := Unit;
```

## Local state

The local state of the Identity Management Engine includes information about the identities it manages.

```juvix
type IdentityInfo := mkIdentityInfo@{
  backend : Backend;
  capabilities : Capabilities;
  commitmentEngine : Option EngineID;
  decryptionEngine : Option EngineID;
};

type IdentityManagementLocalState := mkIdentityManagementLocalState {
  identities : Map EngineID IdentityInfo;
  genDecryptor : Backend -> Decryptor Backend Plaintext Ciphertext;
  genSigner : Backend -> Signer Backend Signable Commitment
};
```

## Timer Handle

```juvix
syntax alias IdentityManagementTimerHandle := Unit;
```

The Identity Management Engine does not require a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Environment summary

```juvix
IdentityManagementEnvironment : Type := EngineEnvironment
  IdentityManagementLocalState
  IdentityManagementMailboxState
  IdentityManagementTimerHandle;
```

## Example of an `Identity Management` environment

<!-- --8<-- [start:environment-example] -->
```juvix extract-module-statements
module identity_management_environment_example;

identityManagementEnvironmentExample : IdentityManagementEnvironment :=
    mkEngineEnvironment@{
      name := "identity_management";
      localState := mkIdentityManagementLocalState@{
        identities := Map.empty;
        genDecryptor := \{_ := mkDecryptor@{
          decrypt := \{_ x := some x};
        }};
        genSigner := \{_ := mkSigner@{
          sign := \{_ x := Ed25519Signature};
        }};
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:environment-example] -->

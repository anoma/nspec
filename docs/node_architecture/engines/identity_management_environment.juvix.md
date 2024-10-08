---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-family
tags:
- identity_management
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.identity_management_environment;

    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.identity_management_overview open;
    import node_architecture.identity_types open;
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
type IdentityInfo := mkIdentityInfo {
  backend : Backend;
  capabilities : Capabilities;
  commitmentEngine : Maybe Address;
  decryptionEngine : Maybe Address;
};

type IdentityManagementLocalState := mkIdentityManagementLocalState {
  identities : Map ExternalIdentity IdentityInfo;
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
  IdentityManagementMsg 
  IdentityManagementMailboxState 
  IdentityManagementTimerHandle;
```

## Example of an `Identity Management` environment

```juvix extract-module-statements
module identity_management_environment_example;

identityManagementEnvironmentExample : IdentityManagementEnvironment :=
    mkEngineEnvironment@{
      name := Left "identity_management";
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

---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- identity_management
- engine-dynamics
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.identity_management_dynamics;

    import prelude open;
    import Stdlib.Data.String.Base open;
    import Stdlib.Data.Bool open;
    import Data.Map open;
    import node_architecture.basics open;
    import node_architecture.identity_types open;
    import system_architecture.identity.identity open hiding {ExternalIdentity};
    import node_architecture.types.engine_dynamics open;
    import node_architecture.types.engine_environment open;
    import node_architecture.engines.identity_management_environment open;
    import node_architecture.engines.identity_management_overview open;
    import node_architecture.engines.decryption_environment open;
    import node_architecture.engines.commitment_environment open;
    import node_architecture.types.anoma_message open;
    import node_architecture.types.anoma_environment open;
    ```

# `Identity Management` Dynamics

## Overview

The dynamics of the Identity Management Engine define how it processes incoming messages (requests) and produces the corresponding responses and actions.

## Action labels

<!-- --8<-- [start:identity-management-action-label] -->
```juvix
type IdentityManagementActionLabel :=
  | -- --8<-- [start:DoGenerateIdentity]
    DoGenerateIdentity {
      backend : Backend;
      params : IDParams;
      capabilities : Capabilities
    }
    -- --8<-- [end:DoGenerateIdentity]
  | -- --8<-- [start:DoConnectIdentity]
    DoConnectIdentity {
      externalIdentity : ExternalIdentity;
      backend : Backend;
      capabilities : Capabilities
    }
    -- --8<-- [end:DoConnectIdentity]
  | -- --8<-- [start:DoDeleteIdentity]
    DoDeleteIdentity {
      externalIdentity : ExternalIdentity;
      backend : Backend
    }
    -- --8<-- [end:DoDeleteIdentity]
;
```
<!-- --8<-- [end:identity-management-action-label] -->

### `DoGenerateIdentity`

!!! quote ""

    --8<-- "./identity_management_dynamics.juvix.md:DoGenerateIdentity"

This action label corresponds to generating a new identity.

??? quote "`DoGenerateIdentity` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | A new identity is created and added to the `identities` map in the local state. The identity includes information about backend, capabilities, and potentially spawned engine references. |
    | Messages to be sent   | A `GenerateIdentityResponse` message is sent to the requester, containing the new identity information including references to spawned engines (if any) or an error message if the identity already exists. |
    | Engines to be spawned | Depending on the requested capabilities, Commitment and/or Decryption engines may be spawned. |
    | Timer updates         | No timers are set or cancelled. |

### `DoConnectIdentity`

!!! quote ""

    --8<-- "./identity_management_dynamics.juvix.md:DoConnectIdentity"

This action label corresponds to connecting to an existing identity.

??? quote "`DoConnectIdentity` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | If successful, a new entry is added to the `identities` map in the local state, linking the requesting address to the external identity's information, filtered by the requested capabilities. |
    | Messages to be sent   | A `ConnectIdentityResponse` message is sent to the requester, confirming the connection and providing references to relevant engines, or an error message if the connection fails (e.g., identity already exists, external identity not found, or requested capabilities not available). |
    | Engines to be spawned | No new engines are spawned. The action reuses existing engine references from the external identity. |
    | Timer updates         | No timers are set or cancelled. |

### `DoDeleteIdentity`

!!! quote ""

    --8<-- "./identity_management_dynamics.juvix.md:DoDeleteIdentity"

This action label corresponds to deleting an existing identity.

??? quote "`DoDeleteIdentity` action effect"

    This action does the following:

    | Aspect | Description |
    |--------|-------------|
    | State update          | The specified identity is removed from the `identities` map in the local state if it exists. |
    | Messages to be sent   | A `DeleteIdentityResponse` message is sent to the requester, confirming the deletion or providing an error message if the identity doesn't exist. |
    | Engines to be spawned | No engines are spawned by this action. |
    | Timer updates         | No timers are set or cancelled. |

## Matchable arguments

<!-- --8<-- [start:identity-management-matchable-argument] -->

```juvix
type IdentityManagementMatchableArgument :=
  | -- --8<-- [start:MessageFrom]
  MessageFrom (Maybe Address) (Maybe MailboxID)
  -- --8<-- [end:MessageFrom]
;
```
<!-- --8<-- [end:identity-management-matchable-argument] -->

### `MessageFrom`

!!! quote ""

    ```
    --8<-- "./docs/node_architecture/engines/identity_management_dynamics.juvix.md:MessageFrom"
    ```

This matchable argument contains the address and mailbox ID of where the response message should be sent.

## Precomputation results

The Identity Management Engine does not require any non-trivial pre-computations.

<!-- --8<-- [start:identity-management-precomputation-entry] -->
```juvix
syntax alias IdentityManagementPrecomputation := Unit;
```
<!-- --8<-- [end:identity-management-precomputation-entry] -->

## Guards

??? quote "Auxiliary Juvix code"

    Type alias for the guard.

    ```juvix
    -- --8<-- [start:identity-management-guard]
    IdentityManagementGuard : Type :=
      Guard
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementMatchableArgument
        IdentityManagementActionLabel
        IdentityManagementPrecomputation;
    -- --8<-- [end:identity-management-guard]

    -- --8<-- [start:identity-management-guard-output]
    IdentityManagementGuardOutput : Type :=
      GuardOutput IdentityManagementMatchableArgument IdentityManagementActionLabel IdentityManagementPrecomputation;
    -- --8<-- [end:identity-management-guard-output]
    ```

### `generateIdentityGuard`

<figure markdown>
```mermaid
flowchart TD
    C{GenerateIdentityRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoGenerateIdentity])
```
<figcaption>generateIdentityGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:generate-identity-guard] -->
```juvix
generateIdentityGuard
  (t : TimestampedTrigger IdentityManagementTimerHandle)
  (env : IdentityManagementEnvironment) : Maybe IdentityManagementGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (MsgIdentityManagement (GenerateIdentityRequest x y z)) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [MessageFrom (just sender) nothing];
                  label := DoGenerateIdentity x y z;
                  other := unit
                });
      }
      | _ := nothing
  };
```
<!-- --8<-- [end:generate-identity-guard] -->

### `connectIdentityGuard`

<figure markdown>
```mermaid
flowchart TD
    C{ConnectIdentityRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoConnectIdentity])
```
<figcaption>connectIdentityGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:connect-identity-guard] -->
```juvix
connectIdentityGuard
  (t : TimestampedTrigger IdentityManagementTimerHandle)
  (env : IdentityManagementEnvironment) : Maybe IdentityManagementGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (MsgIdentityManagement (ConnectIdentityRequest x y z)) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [MessageFrom (just sender) nothing];
                  label := DoConnectIdentity x y z;
                  other := unit
                });
        }
      | _ := nothing
  };
```
<!-- --8<-- [end:connect-identity-guard] -->

### `deleteIdentityGuard`

<figure markdown>
```mermaid
flowchart TD
    C{DeleteIdentityRequest<br>received?}
    C -->|Yes| D[enabled]
    C -->|No| E[not enabled]
    D --> F([DoDeleteIdentity])
```
<figcaption>deleteIdentityGuard flowchart</figcaption>
</figure>

<!-- --8<-- [start:delete-identity-guard] -->
```juvix
deleteIdentityGuard
  (t : TimestampedTrigger IdentityManagementTimerHandle)
  (env : IdentityManagementEnvironment) : Maybe IdentityManagementGuardOutput
  := case getMessageFromTimestampedTrigger t of {
      | just (MsgIdentityManagement (DeleteIdentityRequest x y)) := do {
        sender <- getMessageSenderFromTimestampedTrigger t;
        pure (mkGuardOutput@{
                  args := [MessageFrom (just sender) nothing];
                  label := DoDeleteIdentity x y;
                  other := unit
                });
        }
      | _ := nothing
  };
```
<!-- --8<-- [end:delete-identity-guard] -->

## Action function

??? quote "Auxiliary Juvix code"

    Type alias for the action function.

    ```juvix
    IdentityManagementActionInput : Type :=
      ActionInput
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementMatchableArgument
        IdentityManagementActionLabel
        IdentityManagementPrecomputation;

    IdentityManagementActionEffect : Type :=
      ActionEffect
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementMatchableArgument
        IdentityManagementActionLabel
        IdentityManagementPrecomputation;
    ```

<!-- --8<-- [start:action-function] -->
```juvix
nameStr (name : Name) : String :=
  case name of {
    | Left s := s
    | Right n := natToString n
  };
nameGen (str : String) (name : Name) (addr : Address) : Name :=
  Left (nameStr name ++str "_" ++str str ++str "_" ++str nameStr addr);
makeDecryptEnv (env : IdentityManagementEnvironment) (backend' : Backend) (addr : Address): DecryptionEnvironment :=
  let
    local := EngineEnvironment.localState env;
  in mkEngineEnvironment@{
      name := nameGen "decryptor" (EngineEnvironment.name env) addr;
      localState := mkDecryptionLocalState@{
        decryptor := IdentityManagementLocalState.genDecryptor local backend';
        backend := backend';
      };
      -- The Decryption engine has one empty mailbox.
      mailboxCluster := fromList [(mkPair 0 (mkMailbox@{
        messages := [];
        mailboxState := nothing;
      }))];
      acquaintances := Set.empty;
      timers := []
    };
makeCommitmentEnv (env : IdentityManagementEnvironment) (backend' : Backend) (addr : Address): CommitmentEnvironment :=
    let
      local := EngineEnvironment.localState env;
    in mkEngineEnvironment@{
      name := nameGen "committer" (EngineEnvironment.name env) addr;
      localState := mkCommitmentLocalState@{
        signer := IdentityManagementLocalState.genSigner local backend';
        backend := backend';
      };
      -- The Commitment engine has one empty mailbox.
      mailboxCluster := fromList [(mkPair 0 (mkMailbox@{
        messages := [];
        mailboxState := nothing;
      }))];
      acquaintances := Set.empty;
      timers := []
    };

hasCommitCapability (capabilities : Capabilities) : Bool :=
  case capabilities of {
    | CapabilityCommit := true
    | CapabilityCommitAndDecrypt := true
    | _ := false
  };

hasDecryptCapability (capabilities : Capabilities) : Bool :=
  case capabilities of {
    | CapabilityDecrypt := true
    | CapabilityCommitAndDecrypt := true
    | _ := false
  };

isSubsetCapabilities (requested : Capabilities) (available : Capabilities) : Bool :=
  (not (hasCommitCapability requested) || hasCommitCapability available) 
  && (not (hasDecryptCapability requested) || hasDecryptCapability available);

updateIdentityAndSpawnEngines (env : IdentityManagementEnvironment) (backend' : Backend) (whoAsked : Address) (identityInfo : IdentityInfo) (capabilities' : Capabilities) : Pair IdentityInfo (List Env) :=
  case capabilities' of {
    | CapabilityCommitAndDecrypt :=
        let commitmentEnv := makeCommitmentEnv env backend' whoAsked;
            commitmentEngineName := EngineEnvironment.name commitmentEnv;
            decryptionEnv := makeDecryptEnv env backend' whoAsked;
            decryptionEngineName := EngineEnvironment.name decryptionEnv;
            spawnedEngines := [EnvCommitment commitmentEnv; EnvDecryption decryptionEnv];
            updatedIdentityInfo1 := identityInfo@IdentityInfo{
              commitmentEngine := just commitmentEngineName;
              decryptionEngine := just decryptionEngineName
            };
        in mkPair updatedIdentityInfo1 spawnedEngines
    | CapabilityCommit :=
        let commitmentEnv := makeCommitmentEnv env backend' whoAsked;
            commitmentEngineName := EngineEnvironment.name commitmentEnv;
            spawnedEngines := [EnvCommitment commitmentEnv];
            updatedIdentityInfo1 := identityInfo@IdentityInfo{
              commitmentEngine := just commitmentEngineName
            };
        in mkPair updatedIdentityInfo1 spawnedEngines
    | CapabilityDecrypt :=
        let decryptionEnv := makeDecryptEnv env backend' whoAsked;
            decryptionEngineName := EngineEnvironment.name decryptionEnv;
            spawnedEngines := [EnvDecryption decryptionEnv];
            updatedIdentityInfo1 := identityInfo@IdentityInfo{
              decryptionEngine := just decryptionEngineName
            };
        in mkPair updatedIdentityInfo1 spawnedEngines
  };

copyEnginesForCapabilities (env : IdentityManagementEnvironment) (whoAsked : Address) (externalIdentityInfo : IdentityInfo) (requestedCapabilities : Capabilities) : IdentityInfo :=
  let newIdentityInfo := mkIdentityInfo@{
        backend := IdentityInfo.backend externalIdentityInfo;
        capabilities := requestedCapabilities;
        commitmentEngine :=
          case hasCommitCapability requestedCapabilities of {
            | true := IdentityInfo.commitmentEngine externalIdentityInfo
            | false := nothing
          };
        decryptionEngine :=
          case hasDecryptCapability requestedCapabilities of {
            | true := IdentityInfo.decryptionEngine externalIdentityInfo
            | false := nothing
          }
      };
  in newIdentityInfo;

identityManagementAction (input : IdentityManagementActionInput) : IdentityManagementActionEffect :=
  let env := ActionInput.env input;
      out := ActionInput.guardOutput input;
      local := EngineEnvironment.localState env;
      identities := IdentityManagementLocalState.identities local;
  in
  case GuardOutput.label out of {
    | DoGenerateIdentity backend' params' capabilities' := 
      case GuardOutput.args out of {
        | (MessageFrom (just whoAsked) _) :: _ := 
            case Map.lookup whoAsked identities of {
              | just _ := 
                  -- Identity already exists, return error
                  let responseMsg := GenerateIdentityResponse@{
                    commitmentEngine := nothing;
                    decryptionEngine := nothing;
                    externalIdentity := whoAsked;
                    error := just "Identity already exists"
                  };
                  in mkActionEffect@{
                    newEnv := env;
                    producedMessages := [mkEnvelopedMessage@{
                      sender := just (EngineEnvironment.name env);
                      packet := mkMessagePacket@{
                        target := whoAsked;
                        mailbox := just 0;
                        message := MsgIdentityManagement responseMsg
                      }
                    }];
                    timers := [];
                    spawnedEngines := []
                  }
              | nothing := 
                  -- Proceed to create identity
                  let identityInfo := mkIdentityInfo@{
                        backend := backend';
                        capabilities := capabilities';
                        commitmentEngine := nothing;
                        decryptionEngine := nothing
                      };
                      -- Update identityInfo and spawnedEngines based on capabilities
                      pair' := updateIdentityAndSpawnEngines env backend' whoAsked identityInfo capabilities';
                      updatedIdentityInfo := fst pair';
                      spawnedEnginesFinal := snd pair';
                      updatedIdentities := Map.insert whoAsked updatedIdentityInfo identities;
                      newLocalState := local@IdentityManagementLocalState{
                        identities := updatedIdentities
                      };
                      newEnv' := env@EngineEnvironment{
                        localState := newLocalState
                      };
                      responseMsg := GenerateIdentityResponse@{
                        commitmentEngine := IdentityInfo.commitmentEngine updatedIdentityInfo;
                        decryptionEngine := IdentityInfo.decryptionEngine updatedIdentityInfo;
                        externalIdentity := whoAsked;
                        error := nothing
                      };
                  in mkActionEffect@{
                    newEnv := newEnv';
                    producedMessages := [mkEnvelopedMessage@{
                      sender := just (EngineEnvironment.name env);
                      packet := mkMessagePacket@{
                        target := whoAsked;
                        mailbox := just 0;
                        message := MsgIdentityManagement responseMsg
                      }
                    }];
                    timers := [];
                    spawnedEngines := spawnedEnginesFinal
                  }
            }
        | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }

    | DoConnectIdentity externalIdentity' backend' capabilities' :=
      case GuardOutput.args out of {
        | (MessageFrom (just whoAsked) _) :: _ :=
            -- Check if whoAsked already exists
            case Map.lookup whoAsked identities of {
              | just _ :=
                  -- whoAsked already exists, return error
                  let responseMsg := ConnectIdentityResponse@{
                    commitmentEngine := nothing;
                    decryptionEngine := nothing;
                    error := just "Identity already exists"
                  };
                  in mkActionEffect@{
                    newEnv := env;
                    producedMessages := [mkEnvelopedMessage@{
                      sender := just (EngineEnvironment.name env);
                      packet := mkMessagePacket@{
                        target := whoAsked;
                        mailbox := just 0;
                        message := MsgIdentityManagement responseMsg
                      }
                    }];
                    timers := [];
                    spawnedEngines := []
                  }
              | nothing :=
                  -- whoAsked does not exist, proceed
                  case Map.lookup externalIdentity' identities of {
                    | nothing :=
                        -- externalIdentity' does not exist, return error
                        let responseMsg := ConnectIdentityResponse@{
                          commitmentEngine := nothing;
                          decryptionEngine := nothing;
                          error := just "External identity not found"
                        };
                        in mkActionEffect@{
                          newEnv := env;
                          producedMessages := [mkEnvelopedMessage@{
                            sender := just (EngineEnvironment.name env);
                            packet := mkMessagePacket@{
                              target := whoAsked;
                              mailbox := just 0;
                              message := MsgIdentityManagement responseMsg
                            }
                          }];
                          timers := [];
                          spawnedEngines := []
                        }
                    | just externalIdentityInfo :=
                        -- Compare capabilities
                        let externalCapabilities := IdentityInfo.capabilities externalIdentityInfo;
                            requestedCapabilities := capabilities';
                            isSubset := isSubsetCapabilities requestedCapabilities externalCapabilities;
                        in
                        case isSubset of {
                          | true :=
                              -- Capabilities are a subset, proceed
                              -- Copy the engine information for the requested capabilities
                              let newIdentityInfo := copyEnginesForCapabilities env whoAsked externalIdentityInfo requestedCapabilities;
                                  updatedIdentities := Map.insert whoAsked newIdentityInfo identities;
                                  newLocalState := local@IdentityManagementLocalState{
                                    identities := updatedIdentities
                                  };
                                  newEnv' := env@EngineEnvironment{
                                    localState := newLocalState
                                  };
                                  responseMsg := ConnectIdentityResponse@{
                                    commitmentEngine := IdentityInfo.commitmentEngine newIdentityInfo;
                                    decryptionEngine := IdentityInfo.decryptionEngine newIdentityInfo;
                                    error := nothing
                                  };
                              in mkActionEffect@{
                                newEnv := newEnv';
                                producedMessages := [mkEnvelopedMessage@{
                                  sender := just (EngineEnvironment.name env);
                                  packet := mkMessagePacket@{
                                    target := whoAsked;
                                    mailbox := just 0;
                                    message := MsgIdentityManagement responseMsg
                                  }
                                }];
                                timers := [];
                                spawnedEngines := []
                              }
                          | false :=
                              -- Capabilities not a subset, return error
                              let responseMsg := ConnectIdentityResponse@{
                                commitmentEngine := nothing;
                                decryptionEngine := nothing;
                                error := just "Requested capabilities not available"
                              };
                              in mkActionEffect@{
                                newEnv := env;
                                producedMessages := [mkEnvelopedMessage@{
                                  sender := just (EngineEnvironment.name env);
                                  packet := mkMessagePacket@{
                                    target := whoAsked;
                                    mailbox := just 0;
                                    message := MsgIdentityManagement responseMsg
                                  }
                                }];
                                timers := [];
                                spawnedEngines := []
                              }
                        }
                  }
            }
        | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }

    | DoDeleteIdentity externalIdentity' backend' := 
      case GuardOutput.args out of {
        | (MessageFrom (just whoAsked) _) :: _ :=
            -- Check if the identity exists
            case Map.lookup whoAsked identities of {
              | nothing :=
                  -- Identity does not exist, return error
                  let responseMsg := DeleteIdentityResponse@{
                    error := just "Identity does not exist"
                  };
                  in mkActionEffect@{
                    newEnv := env;
                    producedMessages := [mkEnvelopedMessage@{
                      sender := just (EngineEnvironment.name env);
                      packet := mkMessagePacket@{
                        target := whoAsked;
                        mailbox := just 0;
                        message := MsgIdentityManagement responseMsg
                      }
                    }];
                    timers := [];
                    spawnedEngines := []
                  }
              | just _ :=
                  -- Identity exists, proceed to delete
                  let updatedIdentities := Map.delete whoAsked identities;
                      newLocalState := local@IdentityManagementLocalState{
                        identities := updatedIdentities
                      };
                      newEnv' := env@EngineEnvironment{
                        localState := newLocalState
                      };
                      responseMsg := DeleteIdentityResponse@{
                        error := nothing
                      };
                  in mkActionEffect@{
                    newEnv := newEnv';
                    producedMessages := [mkEnvelopedMessage@{
                      sender := just (EngineEnvironment.name env);
                      packet := mkMessagePacket@{
                        target := whoAsked;
                        mailbox := just 0;
                        message := MsgIdentityManagement responseMsg
                      }
                    }];
                    timers := [];
                    spawnedEngines := []
                  }
            }
        | _ := mkActionEffect@{newEnv := env; producedMessages := []; timers := []; spawnedEngines := []}
      }
  };
```
<!-- --8<-- [end:action-function] -->

## Conflict solver

```juvix
identityManagementConflictSolver : Set IdentityManagementMatchableArgument -> List (Set IdentityManagementMatchableArgument)
  | _ := [];
```

## `Identity Management` Engine Summary

--8<-- "./docs/node_architecture/engines/identity_management.juvix.md:identity-management-engine-family"

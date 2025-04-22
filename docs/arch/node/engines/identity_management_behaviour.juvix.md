---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - identity-management
  - behaviour
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management_behaviour;

    import prelude open;
    import arch.node.engines.commitment_config open;
    import arch.node.engines.decryption_config open;
    import arch.node.engines.commitment_environment open;
    import arch.node.engines.decryption_environment open;
    import arch.node.engines.identity_management_environment open;
    import arch.node.engines.identity_management_messages open;
    import arch.node.engines.identity_management_config open;
    import arch.node.types.anoma as Anoma open;
    import arch.node.types.engine open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
    ```
---

# Identity Management Behaviour
---

## Overview

The behaviour of the Identity Management Engine defines how it coordinates
committing/signing and decrypting operations through the spawning of engines for
these functions along with maintaining a database which may be modified through
the creation, connection, and deletion of identities associated with specific
capabilities.

## Identity Management Action Flowcharts

### `generateIdentityAction` flowchart

<figure markdown>

```mermaid
flowchart TD
    Start([Generate Request]) --> MsgReq[MsgIdentityManagementGenerateIdentityRequest<br/>backend: Backend<br/>params: IDParams<br/>capabilities: Capabilities]

    subgraph Guard["generateIdentityGuard"]
        MsgReq --> ValidType{Is message type<br/>GenerateIdentityRequest?}
        ValidType -->|No| Reject([Reject Request])
        ValidType -->|Yes| ActionEntry[Enter Action Phase]
    end

    ActionEntry --> Action

    subgraph Action["generateIdentityAction"]
        direction TB
        Check{Identity already<br/>exists?}
        Check -->|Yes| ErrExists[Create Error Reply]
        Check -->|No| Create[Create new identity info]
        Create --> SpawnEngines{Which capabilities?}
        SpawnEngines -->|Commit| SpawnCommit[Spawn Commitment Engine]
        SpawnEngines -->|Decrypt| SpawnDecrypt[Spawn Decryption Engine]
        SpawnEngines -->|Both| SpawnBoth[Spawn Both Engines]
        SpawnCommit & SpawnDecrypt & SpawnBoth --> UpdateState[Update registry]
    end

    UpdateState --> Reply[Success Reply<br/>with engine IDs]
    ErrExists --> ErrReply[Error Reply]
    Reply & ErrReply --> Client([Return to Client])
```

<figcaption markdown="span">

`generateIdentityAction` flowchart

</figcaption>
</figure>

#### Explanation

1. **Initial Request**
   - A client sends a `MsgIdentityManagementGenerateIdentityRequest` containing:
     - `backend`: Specifies backend to be used
     - `params`: Cryptographic parameters
     - `capabilities`: Which capabilities are needed (commit, decrypt, or both)
   - The requesting identity must not already exist in the system

2. **Guard Phase** (`generateIdentityGuard`)
   - Validates incoming message structure and type
   - Validation steps:
     - Verifies message type is `MsgIdentityManagementGenerateIdentityRequest`
     - If validation fails, request is rejected immediately
     - On success, passes control to `generateIdentityActionLabel`

3. **Action Phase** (`generateIdentityAction`)
   - Processes valid generation requests through these steps:
     - Checks if requesting identity already exists in registry
     - Creates new identity info with specified backend and capabilities
     - Spawns appropriate engine(s) based on requested capabilities
     - Updates identity registry with new identity and engine references
     - Constructs appropriate response based on result

4. **Reply Generation**
   - **Successful Case**
     - Creates `MsgIdentityManagementGenerateIdentityReply` with:
       - `commitmentEngine`: Engine ID if commit capability requested, None otherwise
       - `decryptionEngine`: Engine ID if decrypt capability requested, None otherwise
       - `externalIdentity`: ID of the newly created identity
       - `err`: None
   - **Error Case**
     - Creates `MsgIdentityManagementGenerateIdentityReply` with:
       - `commitmentEngine`: None
       - `decryptionEngine`: None
       - `externalIdentity`: Requester's ID
       - `err`: Some "Identity already exists"

5. **Reply Delivery**
   - Reply is sent back to the original requester
   - Uses mailbox 0 (default mailbox for responses)

### `connectIdentityAction` flowchart

<figure markdown>

```mermaid
flowchart TD
    Start([Connect Request]) --> MsgReq[MsgIdentityManagementConnectIdentityRequest<br/>externalIdentity: EngineID<br/>backend: Backend<br/>capabilities: Capabilities]

    subgraph Guard["connectIdentityGuard"]
        MsgReq --> ValidType{Is message type<br/>ConnectIdentityRequest?}
        ValidType -->|No| Reject([Reject Request])
        ValidType -->|Yes| ActionEntry[Enter Action Phase]
    end

    ActionEntry --> Action

    subgraph Action["connectIdentityAction"]
        direction TB
        Check{Requesting Identity<br/>exists?}
        Check -->|Yes| ErrExists[Create Error Reply]
        Check -->|No| FindExternal{External Identity<br/>exists?}
        FindExternal -->|No| ErrNotFound[Error: Not Found]
        FindExternal -->|Yes| CheckCaps{Requested capabilities<br/>subset of original?}
        CheckCaps -->|No| ErrCaps[Error: Invalid Capabilities]
        CheckCaps -->|Yes| CopyEngines[Copy Engine References]
        CopyEngines --> UpdateState[Update registry]
    end

    UpdateState --> Reply[Success Reply<br/>with engine IDs]
    ErrExists & ErrNotFound & ErrCaps --> ErrReply[Error Reply]
    Reply & ErrReply --> Client([Return to Client])
```

<figcaption markdown="span">

`connectIdentityAction` flowchart

</figcaption>
</figure>

#### Explanation

1. **Initial Request**
   - A client sends a `MsgIdentityManagementConnectIdentityRequest` containing:
     - `externalIdentity`: ID of the existing identity to connect to
     - `backend`: Backend to use
     - `capabilities`: Which subset of the original identity's capabilities are requested
   - The requesting identity must not already exist in the system
   - The external identity must exist and have at least the requested capabilities

2. **Guard Phase** (`connectIdentityGuard`)
   - Validates incoming message structure and type
   - Validation steps:
     - Verifies message type is `MsgIdentityManagementConnectIdentityRequest`
     - If validation fails, request is rejected immediately
     - On success, passes control to `connectIdentityActionLabel`

3. **Action Phase** (`connectIdentityAction`)
   - Processes valid connection requests through these steps:
     - Verifies requesting identity doesn't already exist
     - Checks if external identity exists in registry
     - Validates requested capabilities are subset of original
     - Copies relevant engine references based on capabilities
     - Updates identity registry with new connected identity
     - Constructs appropriate response based on result

4. **Reply Generation**
   - **Successful Case**
     - Creates `MsgIdentityManagementConnectIdentityReply` with:
       - `commitmentEngine`: Copied engine ID if commit capability requested, None otherwise
       - `decryptionEngine`: Copied engine ID if decrypt capability requested, None otherwise
       - `err`: None
   - **Error Cases**
     - Creates `MsgIdentityManagementConnectIdentityReply` with:
       - `commitmentEngine`: None
       - `decryptionEngine`: None
       - `err`: Some error message:
         - "Identity already exists" if requesting identity exists
         - "External identity not found" if target doesn't exist
         - "Capabilities not available" if capability subset invalid

5. **Reply Delivery**
   - Reply is sent back to the original requester
   - Uses mailbox 0 (default mailbox for responses)

### `deleteIdentityAction` flowchart

<figure markdown>

```mermaid
flowchart TD
    Start([Delete Request]) --> MsgReq[MsgIdentityManagementDeleteIdentityRequest<br/>externalIdentity: EngineID<br/>backend: Backend]

    subgraph Guard["deleteIdentityGuard"]
        MsgReq --> ValidType{Is message type<br/>DeleteIdentityRequest?}
        ValidType -->|No| Reject([Reject Request])
        ValidType -->|Yes| ActionEntry[Enter Action Phase]
    end

    ActionEntry --> Action

    subgraph Action["deleteIdentityAction"]
        direction TB
        Check{Identity exists?}
        Check -->|No| ErrNoExist[Create Error Reply]
        Check -->|Yes| Delete[Remove from registry]
    end

    Delete --> Reply[Success Reply]
    ErrNoExist --> ErrReply[Error Reply]
    Reply & ErrReply --> Client([Return to Client])

    style Guard fill:#f0f7ff,stroke:#333,stroke-width:2px
    style Action fill:#fff7f0,stroke:#333,stroke-width:2px
```

<figcaption markdown="span">

`deleteIdentityAction` flowchart

</figcaption>
</figure>

#### Explanation

1. **Initial Request**
   - A client sends a `MsgIdentityManagementDeleteIdentityRequest` containing:
     - `externalIdentity`: ID of the identity to delete
     - `backend`: Backend system where the identity exists
   - The identity to be deleted must exist in the system

2. **Guard Phase** (`deleteIdentityGuard`)
   - Validates incoming message structure and type
   - Validation steps:
     - Verifies message type is `MsgIdentityManagementDeleteIdentityRequest`
     - If validation fails, request is rejected immediately
     - On success, passes control to `deleteIdentityActionLabel`

3. **Action Phase** (`deleteIdentityAction`)
   - Processes valid deletion requests through these steps:
     - Verifies identity exists in registry
     - Removes identity and associated engine references from registry
     - Constructs appropriate response based on result

4. **Reply Generation**
   - **Successful Case**
     - Creates `MsgIdentityManagementDeleteIdentityReply` with:
       - `err`: None
   - **Error Case**
     - Creates `MsgIdentityManagementDeleteIdentityReply` with:
       - `err`: Some "Identity does not exist"

5. **Reply Delivery**
   - Reply is sent back to the original requester
   - Uses mailbox 0 (default mailbox for responses)

!!! warning "Important Notes"

    - All spawned engines inherit the backend from the generation request
    - Engine references are managed through the identity management engine's state
    - Capabilities can only be restricted when connecting, never expanded
    - The system maintains a mapping between identities and their associated engine references
    - Each identity maintains its own separate set of engines
    - State updates are atomic - either all parts succeed or none do

## Action arguments

### `MessageFrom`

```juvix
type MessageFrom := mkMessageFrom {
  whoAsked : Option EngineID;
  mailbox : Option MailboxID
};
```

### `IdentityManagementActionArgument`

<!-- --8<-- [start:IdentityManagementActionArgument] -->
```juvix
type IdentityManagementActionArgument :=
  | IdentityManagementActionArgumentMessageFrom MessageFrom;
```
<!-- --8<-- [end:IdentityManagementActionArgument] -->

### `IdentityManagementActionArguments`

<!-- --8<-- [start:identity-management-action-arguments] -->
```juvix
IdentityManagementActionArguments : Type := List IdentityManagementActionArgument;
```
<!-- --8<-- [end:identity-management-action-arguments] -->

## Actions

??? code "Auxiliary Juvix code"

    ### `IdentityManagementAction`

    ```juvix
    IdentityManagementAction : Type :=
      Action
        IdentityManagementLocalCfg
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### `IdentityManagementActionInput`

    ```juvix
    IdentityManagementActionInput : Type :=
      ActionInput
        IdentityManagementLocalCfg
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementActionArguments
        Anoma.Msg;
    ```

    ### `IdentityManagementActionEffect`

    ```juvix
    IdentityManagementActionEffect : Type :=
      ActionEffect
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### IdentityManagementActionExec

    ```juvix
    IdentityManagementActionExec : Type :=
      ActionExec
        IdentityManagementLocalCfg
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### `hasCommitCapability`

    ```juvix
    hasCommitCapability (capabilities : Capabilities) : Bool :=
      case capabilities of {
        | Capabilities.Commit := true
        | Capabilities.CommitAndDecrypt := true
        | _ := false
      };
    ```

    ### `hasDecryptCapability`

    ```juvix
    hasDecryptCapability (capabilities : Capabilities) : Bool :=
      case capabilities of {
        | Capabilities.Decrypt := true
        | Capabilities.CommitAndDecrypt := true
        | _ := false
      };
    ```

    ### `isSubsetCapabilities`

    ```juvix
    isSubsetCapabilities
      (requested : Capabilities)
      (available : Capabilities)
      : Bool :=
      (not (hasCommitCapability requested) || hasCommitCapability available)
      && (not (hasDecryptCapability requested) || hasDecryptCapability available);
    ```

    ### `updateIdentityAndSpawnEngines`

    ```juvix
    updateIdentityAndSpawnEngines
      (env : IdentityManagementEnv)
      (cfg : IdentityManagementCfg)
      (backend' : Backend)
      (whoAsked : EngineID)
      (identityInfo : IdentityInfo)
      (capabilities' : Capabilities)
      : Pair IdentityInfo (List (Pair Cfg Env)) :=
      let decryptionConfig : DecryptionCfg :=
            mkEngineCfg@{
              node := EngineCfg.node cfg;
              name := nameGen "decryptor" (snd whoAsked) whoAsked;
              cfg := mkDecryptionLocalCfg@{
                decryptor := genDecryptor backend';
                backend := backend';
              }
            };
          decryptionEnv : DecryptionEnv :=
            EngineEnv.mk@{
              localState := unit;
              mailboxCluster := Map.empty;
              acquaintances := Set.Set.empty;
              timers := []
            };
          decryptionEng : Pair Cfg Env :=
            mkPair (PreCfg.CfgDecryption decryptionConfig) (PreEnv.EnvDecryption decryptionEnv);
          commitmentConfig : CommitmentCfg :=
            mkEngineCfg@{
              node := EngineCfg.node cfg;
              name := nameGen "committer" (snd whoAsked) whoAsked;
              cfg := mkCommitmentLocalCfg@{
                signer := genSigner backend';
                backend := backend';
              }
            };
          commitmentEnv : CommitmentEnv :=
            EngineEnv.mk@{
              localState := unit;
              mailboxCluster := Map.empty;
              acquaintances := Set.Set.empty;
              timers := []
            };
          commitmentEng : Pair Cfg Env :=
            mkPair (PreCfg.CfgCommitment commitmentConfig) (PreEnv.EnvCommitment commitmentEnv);
      in case capabilities' of {
        | Capabilities.CommitAndDecrypt :=
            let spawnedEngines := [decryptionEng; commitmentEng];
                commitmentEngineName := nameGen "committer" (snd whoAsked) whoAsked;
                decryptionEngineName := nameGen "decryptor" (snd whoAsked) whoAsked;
                updatedIdentityInfo1 := identityInfo@IdentityInfo{
                  commitmentEngine := some (mkPair none commitmentEngineName);
                  decryptionEngine := some (mkPair none decryptionEngineName)
                };
            in mkPair updatedIdentityInfo1 spawnedEngines
        | Capabilities.Commit :=
            let spawnedEngines := [commitmentEng];
                commitmentEngineName := nameGen "committer" (snd whoAsked) whoAsked;
                updatedIdentityInfo1 := identityInfo@IdentityInfo{
                  commitmentEngine := some (mkPair none commitmentEngineName)
                };
            in mkPair updatedIdentityInfo1 spawnedEngines
        | Capabilities.Decrypt :=
            let spawnedEngines := [decryptionEng];
                decryptionEngineName := nameGen "decryptor" (snd whoAsked) whoAsked;
                updatedIdentityInfo1 := identityInfo@IdentityInfo{
                  decryptionEngine := some (mkPair none decryptionEngineName)
                };
            in mkPair updatedIdentityInfo1 spawnedEngines
      };
    ```

    ### `copyEnginesForCapabilities`

    ```juvix
    copyEnginesForCapabilities
      (env : IdentityManagementEnv)
      (whoAsked : EngineID)
      (externalIdentityInfo : IdentityInfo)
      (requestedCapabilities : Capabilities)
      : IdentityInfo :=
      let newIdentityInfo := IdentityInfo.mkIdentityInfo@{
            backend := IdentityInfo.backend externalIdentityInfo;
            capabilities := requestedCapabilities;
            commitmentEngine :=
              case hasCommitCapability requestedCapabilities of {
                | true := IdentityInfo.commitmentEngine externalIdentityInfo
                | false := none
              };
            decryptionEngine :=
              case hasDecryptCapability requestedCapabilities of {
                | true := IdentityInfo.decryptionEngine externalIdentityInfo
                | false := none
              }
          };
      in newIdentityInfo;
    ```

### `generateIdentityAction`

State update
: A new identity is created and added to the identities map if it doesn't exist.

Messages to be sent
: A GenerateIdentityReply message containing the new identity info or error.

Engines to be spawned
: Commitment and/or Decryption engines based on capabilities.

Timer updates
: No timers are set or cancelled.

<!-- --8<-- [start:generateIdentityAction] -->
```juvix
generateIdentityAction
  (input : IdentityManagementActionInput)
  : Option IdentityManagementActionEffect :=
  let
    env := ActionInput.env input;
    local := EngineEnv.localState env;
    identities := IdentityManagementLocalState.identities local;
    trigger := ActionInput.trigger input;
  in case getEngineMsgFromTimestampedTrigger trigger of {
    | some emsg :=
      let whoAsked := EngineMsg.sender emsg;
      in case Map.lookup whoAsked identities of {
        | some _ :=
          some ActionEffect.mkActionEffect@{
            env := env;
            msgs := [EngineMsg.mk@{
              sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
              target := whoAsked;
              mailbox := some 0;
              msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.GenerateIdentityReply
                (ReplyGenerateIdentity.mkReplyGenerateIdentity@{
                  commitmentEngine := none;
                  decryptionEngine := none;
                  externalIdentity := whoAsked;
                  err := some "Identity already exists"
                }))
            }];
            timers := [];
            engines := []
          }
        | none :=
          case emsg of {
            | EngineMsg.mk@{msg := Anoma.PreMsg.MsgIdentityManagement (IdentityManagementMsg.GenerateIdentityRequest (RequestGenerateIdentity.mkRequestGenerateIdentity backend' params' capabilities'))} :=
              let identityInfo := IdentityInfo.mkIdentityInfo@{
                    backend := backend';
                    capabilities := capabilities';
                    commitmentEngine := none;
                    decryptionEngine := none
                  };
                  pair' := updateIdentityAndSpawnEngines env (ActionInput.cfg input) backend' whoAsked identityInfo capabilities';
                  updatedIdentityInfo := fst pair';
                  spawnedEnginesFinal := snd pair';
                  updatedIdentities := Map.insert whoAsked updatedIdentityInfo identities;
                  newLocalState := local@IdentityManagementLocalState{
                    identities := updatedIdentities
                  };
                  newEnv' := env@EngineEnv{
                    localState := newLocalState
                  };
              in some ActionEffect.mkActionEffect@{
                env := newEnv';
                msgs := [EngineMsg.mk@{
                  sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
                  target := whoAsked;
                  mailbox := some 0;
                  msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.GenerateIdentityReply
                    (ReplyGenerateIdentity.mkReplyGenerateIdentity@{
                      commitmentEngine := IdentityInfo.commitmentEngine updatedIdentityInfo;
                      decryptionEngine := IdentityInfo.decryptionEngine updatedIdentityInfo;
                      externalIdentity := whoAsked;
                      err := none
                    }))
                }];
                timers := [];
                engines := spawnedEnginesFinal
              }
            | _ := none
          }
      }
    | _ := none
  };
```
<!-- --8<-- [end:generateIdentityAction] -->

### `connectIdentityAction`

State update
: A new identity is created with copied capabilities if valid.

Messages to be sent
: A `ConnectIdentityReply` message with confirmation or error.

Engines to be spawned
: No new engines are spawned.

Timer updates
: No timers are set or cancelled.

<!-- --8<-- [start:connectIdentityAction] -->
```juvix
connectIdentityAction
  (input : IdentityManagementActionInput)
  : Option IdentityManagementActionEffect :=
  let
    env := ActionInput.env input;
    local := EngineEnv.localState env;
    identities := IdentityManagementLocalState.identities local;
    trigger := ActionInput.trigger input;
  in case getEngineMsgFromTimestampedTrigger trigger of {
    | some emsg :=
      let whoAsked := EngineMsg.sender emsg;
      in case Map.lookup whoAsked identities of {
        | some _ :=
          some ActionEffect.mkActionEffect@{
            env := env;
            msgs := [EngineMsg.mk@{
              sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
              target := whoAsked;
              mailbox := some 0;
              msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.ConnectIdentityReply
                (ReplyConnectIdentity.mkReplyConnectIdentity@{
                  commitmentEngine := none;
                  decryptionEngine := none;
                  err := some "Identity already exists"
                }))
            }];
            timers := [];
            engines := []
          }
        | none :=
          case emsg of {
            | EngineMsg.mk@{msg := Anoma.PreMsg.MsgIdentityManagement (IdentityManagementMsg.ConnectIdentityRequest (RequestConnectIdentity.mkRequestConnectIdentity externalIdentity' backend' capabilities'))} :=
              case Map.lookup externalIdentity' identities of {
                | none :=
                  some ActionEffect.mkActionEffect@{
                    env := env;
                    msgs := [EngineMsg.mk@{
                      sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
                      target := whoAsked;
                      mailbox := some 0;
                      msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.ConnectIdentityReply
                        (ReplyConnectIdentity.mkReplyConnectIdentity@{
                          commitmentEngine := none;
                          decryptionEngine := none;
                          err := some "External identity not found"
                        }))
                    }];
                    timers := [];
                    engines := []
                  }
                | some externalIdentityInfo :=
                  if
                    | isSubsetCapabilities capabilities' (IdentityInfo.capabilities externalIdentityInfo) :=
                      let newIdentityInfo := copyEnginesForCapabilities env whoAsked externalIdentityInfo capabilities';
                          updatedIdentities := Map.insert whoAsked newIdentityInfo identities;
                          newLocalState := local@IdentityManagementLocalState{
                            identities := updatedIdentities
                          };
                          newEnv' := env@EngineEnv{
                            localState := newLocalState
                          };
                      in some ActionEffect.mkActionEffect@{
                        env := newEnv';
                        msgs := [EngineMsg.mk@{
                          sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
                          target := whoAsked;
                          mailbox := some 0;
                          msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.ConnectIdentityReply
                            (ReplyConnectIdentity.mkReplyConnectIdentity@{
                              commitmentEngine := IdentityInfo.commitmentEngine newIdentityInfo;
                              decryptionEngine := IdentityInfo.decryptionEngine newIdentityInfo;
                              err := none
                            }))
                        }];
                        timers := [];
                        engines := []
                      }
                    | else :=
                      some ActionEffect.mkActionEffect@{
                        env := env;
                        msgs := [EngineMsg.mk@{
                          sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
                          target := whoAsked;
                          mailbox := some 0;
                          msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.ConnectIdentityReply
                            (ReplyConnectIdentity.mkReplyConnectIdentity@{
                              commitmentEngine := none;
                              decryptionEngine := none;
                              err := some "Capabilities not available"
                            }))
                        }];
                        timers := [];
                        engines := []
                  }
              }
            | _ := none
          }
      }
    | _ := none
  };
```
<!-- --8<-- [end:connectIdentityAction] -->

### `deleteIdentityAction`

State update
: Removes the specified identity if it exists.

Messages to be sent
: A DeleteIdentityReply message with confirmation or error.

Engines to be spawned
: No engines are spawned.

Timer updates
: No timers are set or cancelled.

<!-- --8<-- [start:deleteIdentityAction] -->
```juvix
deleteIdentityAction
  (input : IdentityManagementActionInput)
  : Option IdentityManagementActionEffect :=
  let
    env := ActionInput.env input;
    local := EngineEnv.localState env;
    identities := IdentityManagementLocalState.identities local;
    trigger := ActionInput.trigger input;
  in case getEngineMsgFromTimestampedTrigger trigger of {
    | some emsg :=
      let whoAsked := EngineMsg.sender emsg;
      in case emsg of {
        | EngineMsg.mk@{msg := Anoma.PreMsg.MsgIdentityManagement (IdentityManagementMsg.DeleteIdentityRequest (RequestDeleteIdentity.mkRequestDeleteIdentity externalIdentity backend'))} :=
          case Map.lookup externalIdentity identities of {
            | none :=
              some ActionEffect.mkActionEffect@{
                env := env;
                msgs := [EngineMsg.mk@{
                  sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
                  target := whoAsked;
                  mailbox := some 0;
                  msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.DeleteIdentityReply
                    (ReplyDeleteIdentity.mkReplyDeleteIdentity@{
                      err := some "Identity does not exist"
                    }))
                }];
                timers := [];
                engines := []
              }
            | some _ :=
              let updatedIdentities := Map.delete externalIdentity identities;
                  newLocalState := local@IdentityManagementLocalState{
                    identities := updatedIdentities
                  };
                  newEnv' := env@EngineEnv{
                    localState := newLocalState
                  };
              in some ActionEffect.mkActionEffect@{
                env := newEnv';
                msgs := [EngineMsg.mk@{
                  sender := getEngineIDFromEngineCfg (ActionInput.cfg input);
                  target := whoAsked;
                  mailbox := some 0;
                  msg := PreMsg.MsgIdentityManagement (IdentityManagementMsg.DeleteIdentityReply
                    (ReplyDeleteIdentity.mkReplyDeleteIdentity@{
                      err := none
                    }))
                }];
                timers := [];
                engines := []
              }
          }
        | _ := none
      }
    | _ := none
  };
```
<!-- --8<-- [end:deleteIdentityAction] -->

### Action Labels

#### `generateIdentityActionLabel`

```juvix
generateIdentityActionLabel : IdentityManagementActionExec := ActionExec.Seq [ generateIdentityAction ];
```

#### `connectIdentityActionLabel`

```juvix
connectIdentityActionLabel : IdentityManagementActionExec := ActionExec.Seq [ connectIdentityAction ];
```

#### `deleteIdentityActionLabel`

```juvix
deleteIdentityActionLabel : IdentityManagementActionExec := ActionExec.Seq [ deleteIdentityAction ];
```

## Guards

??? code "Auxiliary Juvix code"



    ### `IdentityManagementGuard`

    <!-- --8<-- [start:IdentityManagementGuard] -->
    ```juvix
    IdentityManagementGuard : Type :=
      Guard
        IdentityManagementLocalCfg
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:IdentityManagementGuard] -->



    ### `IdentityManagementGuardOutput`

    <!-- --8<-- [start:IdentityManagementGuardOutput] -->
    ```juvix
    IdentityManagementGuardOutput : Type :=
      GuardOutput
        IdentityManagementLocalCfg
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:IdentityManagementGuardOutput] -->



    ### `IdentityManagementGuardEval`

    <!-- --8<-- [start:IdentityManagementGuardEval] -->
    ```juvix
    IdentityManagementGuardEval : Type :=
      GuardEval
        IdentityManagementLocalCfg
        IdentityManagementLocalState
        IdentityManagementMailboxState
        IdentityManagementTimerHandle
        IdentityManagementActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:IdentityManagementGuardEval] -->

### `generateIdentityGuard`

Condition
: Message type is MsgIdentityManagementGenerateIdentityRequest.

<!-- --8<-- [start:generateIdentityGuard] -->
```juvix
generateIdentityGuard
  (trigger : TimestampedTrigger IdentityManagementTimerHandle Anoma.Msg)
  (cfg : IdentityManagementCfg)
  (env : IdentityManagementEnv)
  : Option IdentityManagementGuardOutput :=
  case getEngineMsgFromTimestampedTrigger trigger of {
    | some EngineMsg.mk@{
        msg := Anoma.PreMsg.MsgIdentityManagement (IdentityManagementMsg.GenerateIdentityRequest _)
      } :=
      some GuardOutput.mkGuardOutput@{
        action := generateIdentityActionLabel;
        args := []
      }
    | _ := none
  };
```
<!-- --8<-- [end:generateIdentityGuard] -->

### `connectIdentityGuard`

Condition
: Message type is `MsgIdentityManagementConnectIdentityRequest`.

<!-- --8<-- [start:connectIdentityGuard] -->
```juvix
connectIdentityGuard
  (trigger : TimestampedTrigger IdentityManagementTimerHandle Anoma.Msg)
  (cfg : IdentityManagementCfg)
  (env : IdentityManagementEnv)
  : Option IdentityManagementGuardOutput :=
  case getEngineMsgFromTimestampedTrigger trigger of {
    | some EngineMsg.mk@{
        msg := Anoma.PreMsg.MsgIdentityManagement (IdentityManagementMsg.ConnectIdentityRequest _)
      } :=
      some GuardOutput.mkGuardOutput@{
        action := connectIdentityActionLabel;
        args := []
      }
    | _ := none
  };
```<!-- --8<-- [end:connectIdentityGuard] -->
---

### `deleteIdentityGuard`

Condition
: Message type is `MsgIdentityManagementDeleteIdentityRequest`.

<!-- --8<-- [start:deleteIdentityGuard] -->
```juvix
deleteIdentityGuard
  (trigger : TimestampedTrigger IdentityManagementTimerHandle Anoma.Msg)
  (cfg : IdentityManagementCfg)
  (env : IdentityManagementEnv)
  : Option IdentityManagementGuardOutput :=
  case getEngineMsgFromTimestampedTrigger trigger of {
    | some EngineMsg.mk@{
        msg := Anoma.PreMsg.MsgIdentityManagement (IdentityManagementMsg.DeleteIdentityRequest _)
      } :=
      some GuardOutput.mkGuardOutput@{
        action := deleteIdentityActionLabel;
        args := []
      }
    | _ := none
  };
```<!-- --8<-- [end:deleteIdentityGuard] -->
---

## The Identity Management Behaviour

### `IdentityManagementBehaviour`

<!-- --8<-- [start:IdentityManagementBehaviour] -->
```juvix
IdentityManagementBehaviour : Type :=
  EngineBehaviour
    IdentityManagementLocalCfg
    IdentityManagementLocalState
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```<!-- --8<-- [end:IdentityManagementBehaviour] -->

### Instantiation

<!-- --8<-- [start:identityManagementBehaviour] -->
```juvix
identityManagementBehaviour : IdentityManagementBehaviour :=
  EngineBehaviour.mk@{
    guards := GuardEval.First [
      generateIdentityGuard;
      connectIdentityGuard;
      deleteIdentityGuard
    ]
  };
```
<!-- --8<-- [end:identityManagementBehaviour] -->

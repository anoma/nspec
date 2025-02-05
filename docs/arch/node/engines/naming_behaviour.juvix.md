---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - naming
  - behaviour
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.naming_behaviour;

    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    import arch.node.engines.naming_messages open;
    import arch.node.engines.naming_config open;
    import arch.node.engines.naming_environment open;
    import arch.node.types.anoma as Anoma open;
    ```

# Naming Behaviour

## Overview

The behavior of the Naming Engine defines how it processes incoming messages and
updates its state accordingly.

## Action arguments

### `NamingActionArgumentReplyTo ReplyTo`

```juvix
type ReplyTo := mkReplyTo {
  whoAsked : Option EngineID;
  mailbox : Option MailboxID
};
```

This action argument contains the address and mailbox ID of where the
response message should be sent.

`whoAsked`:
: is the address of the engine that sent the message.

`mailbox`:
: is the mailbox ID where the response message should be sent.

### `NamingActionArgument`

<!-- --8<-- [start:NamingActionArgument] -->
```juvix
type NamingActionArgument :=
  | NamingActionArgumentReplyTo ReplyTo
;
```
<!-- --8<-- [end:NamingActionArgument] -->

### `NamingActionArguments`

<!-- --8<-- [start:naming-action-arguments] -->
```juvix
NamingActionArguments : Type := List NamingActionArgument;
```
<!-- --8<-- [end:naming-action-arguments] -->

## Actions

??? code "Auxiliary Juvix code"

    ### NamingAction

    ```juvix
    NamingAction : Type :=
      Action
        NamingCfg
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        NamingActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### NamingActionInput

    ```juvix
    NamingActionInput : Type :=
      ActionInput
        NamingCfg
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        NamingActionArguments
        Anoma.Msg;
    ```

    ### NamingActionEffect

    ```juvix
    NamingActionEffect : Type :=
      ActionEffect
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### NamingActionExec

    ```juvix
    NamingActionExec : Type :=
      ActionExec
        NamingCfg
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        NamingActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

### `resolveNameAction`

Resolve a name to associated external identities.

State update
: No change to the local state.

Messages to be sent
: A `ReplyResolveName` message is sent to the requester, containing matching external identities.

Engines to be spawned
: No engines are spawned by this action.

Timer updates
: No timers are set or cancelled.

```juvix
resolveNameAction
  (input : NamingActionInput)
  : Option NamingActionEffect :=
  let
    env := ActionInput.env input;
    cfg := ActionInput.cfg input;
    tt := ActionInput.trigger input;
    localState := EngineEnv.localState env;
    identityName := case getEngineMsgFromTimestampedTrigger tt of {
      | some mkEngineMsg@{msg := Anoma.MsgNaming (MsgNamingResolveNameRequest req)} :=
          some (RequestResolveName.identityName req)
      | _ := none
    }
  in case identityName of {
    | some name := let
        matchingEvidence := AVLTree.filter \{evidence :=
          isEqual (Ord.cmp (IdentityNameEvidence.identityName evidence) name)
        } (NamingLocalState.evidenceStore localState);
        identities := Set.fromList (map \{evidence :=
          IdentityNameEvidence.externalIdentity evidence
        } (Set.toList matchingEvidence));
        responseMsg := mkReplyResolveName@{
          externalIdentities := identities;
          err := none
        }
      in case getEngineMsgFromTimestampedTrigger tt of {
        | some emsg := some mkActionEffect@{
            env := env;
            msgs := [mkEngineMsg@{
              sender := getEngineIDFromEngineCfg cfg;
              target := EngineMsg.sender emsg;
              mailbox := some 0;
              msg := Anoma.MsgNaming (MsgNamingResolveNameReply responseMsg)
            }];
            timers := [];
            engines := []
          }
        | _ := none
      }
    | _ := none
  };
```

### `submitNameEvidenceAction`

Submit new name evidence.

State update
: If the evidence doesn't already exist and is valid, it's added to the `evidenceStore`.

Messages to be sent
: A response message is sent to the requester, confirming submission or indicating an error.

Engines to be spawned
: No engines are spawned by this action.

Timer updates
: No timers are set or cancelled.

```juvix
submitNameEvidenceAction
  (input : NamingActionInput)
  : Option NamingActionEffect :=
  let
    env := ActionInput.env input;
    cfg := ActionInput.cfg input;
    tt := ActionInput.trigger input;
    localState := EngineEnv.localState env;
    evidence := case getEngineMsgFromTimestampedTrigger tt of {
      | some mkEngineMsg@{msg := Anoma.MsgNaming (MsgNamingSubmitNameEvidenceRequest req)} :=
          some (RequestSubmitNameEvidence.evidence req)
      | _ := none
    }
  in case evidence of {
    | some ev := let
        isValid := verifyEvidence ev;
        alreadyExists := case isValid of {
          | true := isElement \{a b := a && b} true (map \{e :=
              isEqual (Ord.cmp e ev)
            } (Set.toList (NamingLocalState.evidenceStore localState)))
          | false := false
        };
        newEnv := case isValid && (not alreadyExists) of {
          | true := env@EngineEnv{
              localState := localState@NamingLocalState{
                evidenceStore := Set.insert ev (NamingLocalState.evidenceStore localState)
              }
            }
          | false := env
        };
        responseMsg := mkReplySubmitNameEvidence@{
          err := case isValid of {
            | false := some "Invalid evidence"
            | true := case alreadyExists of {
                | true := some "Evidence already exists"
                | false := none
              }
          }
        }
      in case getEngineMsgFromTimestampedTrigger tt of {
        | some emsg := some mkActionEffect@{
            env := newEnv;
            msgs := [mkEngineMsg@{
              sender := getEngineIDFromEngineCfg cfg;
              target := EngineMsg.sender emsg;
              mailbox := some 0;
              msg := Anoma.MsgNaming (MsgNamingSubmitNameEvidenceReply responseMsg)
            }];
            timers := [];
            engines := []
          }
        | _ := none
      }
    | _ := none
  };
```

### `queryNameEvidenceAction`

Query name evidence for a specific external identity.

State update
: No change to the local state.

Messages to be sent
: A `ReplyQueryNameEvidence` message is sent to the requester, containing relevant evidence.

Engines to be spawned
: No engines are spawned by this action.

Timer updates
: No timers are set or cancelled.

```juvix
queryNameEvidenceAction
  (input : NamingActionInput)
  : Option NamingActionEffect :=
  let
    env := ActionInput.env input;
    cfg := ActionInput.cfg input;
    tt := ActionInput.trigger input;
    localState := EngineEnv.localState env;
    externalIdentity := case getEngineMsgFromTimestampedTrigger tt of {
      | some mkEngineMsg@{msg := Anoma.MsgNaming (MsgNamingQueryNameEvidenceRequest req)} :=
          some (RequestQueryNameEvidence.externalIdentity req)
      | _ := none
    }
  in case externalIdentity of {
    | some extId := let
        relevantEvidence := AVLTree.filter \{evidence :=
          isEqual (Ord.cmp (IdentityNameEvidence.externalIdentity evidence) extId)
        } (NamingLocalState.evidenceStore localState);
        responseMsg := mkReplyQueryNameEvidence@{
          externalIdentity := extId;
          evidence := relevantEvidence;
          err := none
        }
      in case getEngineMsgFromTimestampedTrigger tt of {
        | some emsg := some mkActionEffect@{
            env := env;
            msgs := [mkEngineMsg@{
              sender := getEngineIDFromEngineCfg cfg;
              target := EngineMsg.sender emsg;
              mailbox := some 0;
              msg := Anoma.MsgNaming (MsgNamingQueryNameEvidenceReply responseMsg)
            }];
            timers := [];
            engines := []
          }
        | _ := none
      }
    | _ := none
  };
```

## Action Labels

### `resolveNameActionLabel`

```juvix
resolveNameActionLabel : NamingActionExec := Seq [ resolveNameAction ];
```

### `submitNameEvidenceActionLabel`

```juvix
submitNameEvidenceActionLabel : NamingActionExec := Seq [ submitNameEvidenceAction ];
```

### `queryNameEvidenceActionLabel`

```juvix
queryNameEvidenceActionLabel : NamingActionExec := Seq [ queryNameEvidenceAction ];
```

## Guards

??? code "Auxiliary Juvix code"

    ### `NamingGuard`

    <!-- --8<-- [start:NamingGuard] -->
    ```juvix
    NamingGuard : Type :=
      Guard
        NamingCfg
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        NamingActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:NamingGuard] -->

    ### `NamingGuardOutput`

    <!-- --8<-- [start:NamingGuardOutput] -->
    ```juvix
    NamingGuardOutput : Type :=
      GuardOutput
        NamingCfg
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        NamingActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:NamingGuardOutput] -->

    ### `NamingGuardEval`

    <!-- --8<-- [start:NamingGuardEval] -->
    ```juvix
    NamingGuardEval : Type :=
      GuardEval
        NamingCfg
        NamingLocalState
        NamingMailboxState
        NamingTimerHandle
        NamingActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:NamingGuardEval] -->

### `resolveNameGuard`

Condition
: Message type is `MsgNamingResolveNameRequest`.

<!-- --8<-- [start:resolveNameGuard] -->
```juvix
resolveNameGuard
  (tt : TimestampedTrigger NamingTimerHandle Anoma.Msg)
  (cfg : EngineCfg NamingCfg)
  (env : NamingEnv)
  : Option NamingGuardOutput :=
  case getEngineMsgFromTimestampedTrigger tt of {
    | some mkEngineMsg@{
        msg := Anoma.MsgNaming (MsgNamingResolveNameRequest _)
      } := some mkGuardOutput@{
        action := resolveNameActionLabel;
        args := []
      }
    | _ := none
  };
```
<!-- --8<-- [end:resolveNameGuard] -->

### `submitNameEvidenceGuard`

Condition
: Message type is `MsgNamingSubmitNameEvidenceRequest`.

<!-- --8<-- [start:submitNameEvidenceGuard] -->
```juvix
submitNameEvidenceGuard
  (tt : TimestampedTrigger NamingTimerHandle Anoma.Msg)
  (cfg : EngineCfg NamingCfg)
  (env : NamingEnv)
  : Option NamingGuardOutput :=
  case getEngineMsgFromTimestampedTrigger tt of {
    | some mkEngineMsg@{
        msg := Anoma.MsgNaming (MsgNamingSubmitNameEvidenceRequest _)
      } := some mkGuardOutput@{
        action := submitNameEvidenceActionLabel;
        args := []
      }
    | _ := none
  };
```
<!-- --8<-- [end:submitNameEvidenceGuard] -->

### `queryNameEvidenceGuard`

Condition
: Message type is `MsgNamingQueryNameEvidenceRequest`.

<!-- --8<-- [start:queryNameEvidenceGuard] -->
```juvix
queryNameEvidenceGuard
  (tt : TimestampedTrigger NamingTimerHandle Anoma.Msg)
  (cfg : EngineCfg NamingCfg)
  (env : NamingEnv)
  : Option NamingGuardOutput :=
  case getEngineMsgFromTimestampedTrigger tt of {
    | some mkEngineMsg@{
        msg := Anoma.MsgNaming (MsgNamingQueryNameEvidenceRequest _)
      } := some mkGuardOutput@{
        action := queryNameEvidenceActionLabel;
        args := []
      }
    | _ := none
  };
```
<!-- --8<-- [end:queryNameEvidenceGuard] -->

## The Naming Behaviour

### `NamingBehaviour`

<!-- --8<-- [start:NamingBehaviour] -->
```juvix
NamingBehaviour : Type :=
  EngineBehaviour
    NamingCfg
    NamingLocalState
    NamingMailboxState
    NamingTimerHandle
    NamingActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:NamingBehaviour] -->

### Instantiation

<!-- --8<-- [start:namingBehaviour] -->
```juvix
namingBehaviour : NamingBehaviour :=
  mkEngineBehaviour@{
    guards :=
      First [
        resolveNameGuard;
        submitNameEvidenceGuard;
        queryNameEvidenceGuard
      ];
  };
```
<!-- --8<-- [end:namingBehaviour] -->

## Naming Action Flowcharts

### `resolveNameAction` flowchart

<figure markdown>

```mermaid
flowchart TD
  MSG>MsgNamingResolveNameRequest]
  A(resolveNameAction)
  RES>MsgNamingResolveNameReply<br/>externalIdentities]

  MSG --resolveNameGuard--> A --resolveNameActionLabel--> RES
```

<figcaption markdown="span">
`resolveNameAction` flowchart
</figcaption>
</figure>

### `submitNameEvidenceAction` flowchart

<figure markdown>

```mermaid
flowchart TD
  MSG>MsgNamingSubmitNameEvidenceRequest]
  A(submitNameEvidenceAction)
  subgraph E[Effects]
    ES[(State update if valid<br>evidenceStore += evidence)]
    EM>MsgNamingSubmitNameEvidenceReply<br/>error?]
  end

  MSG --submitNameEvidenceGuard--> A --submitNameEvidenceActionLabel--> E
```

<figcaption markdown="span">
`submitNameEvidenceAction` flowchart
</figcaption>
</figure>

### `queryNameEvidenceAction` flowchart

<figure markdown>

```mermaid
flowchart TD
  MSG>MsgNamingQueryNameEvidenceRequest]
  A(queryNameEvidenceAction)
  RES>MsgNamingQueryNameEvidenceReply<br/>evidence]

  MSG --queryNameEvidenceGuard--> A --queryNameEvidenceActionLabel--> RES
```

<figcaption markdown="span">
`queryNameEvidenceAction` flowchart
</figcaption>
</figure>

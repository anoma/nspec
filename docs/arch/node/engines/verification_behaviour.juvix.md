---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - verification
  - behaviour
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.verification_behaviour;

    import prelude open;
    import arch.node.types.messages open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
    import arch.node.types.engine open;
    import arch.node.engines.verification_config open;
    import arch.node.engines.verification_environment open;
    import arch.node.engines.verification_messages open;
    import arch.node.engines.signs_for_messages open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.anoma as Anoma open;
    ```

# Verification Behaviour

## Overview

The behavior of the Verification Engine defines how it processes incoming verification
requests and produces the corresponding responses.

## Verification Action Flowchart

### `verifyAction` flowchart

<figure markdown>

```mermaid
flowchart TD
    Start([Client Request]) --> MsgReq[MsgVerificationRequest<br/>data: Signable<br/>commitment: Commitment<br/>externalIdentity: ExternalIdentity<br/>useSignsFor: Bool]

    subgraph Guard["verifyGuard"]
        MsgReq --> ValidType{Is message type<br/>VerificationRequest?}
        ValidType -->|No| Reject([Reject Request])
        ValidType -->|Yes| ActionEntry[Enter Action Phase]
    end

    ActionEntry --> Action

    subgraph Action["verifyAction"]
        direction TB
        SignsFor{useSignsFor<br/>flag?}
        SignsFor -->|No| DirectVerify[Verify using configured<br/>verifier]
        SignsFor -->|Yes| CheckPending{Existing requests<br/>for this identity?}

        CheckPending -->|Yes| StorePending[Add to pending<br/>request list only]
        CheckPending -->|No| SendAndStore[Send SignsFor request<br/>and store in pending]

        DirectVerify --> Response1[Prepare immediate response]
    end

    Response1 --> MsgResp1[MsgVerificationReply<br/>result: Bool<br/>err: none]
    SendAndStore --> SignsForQuery[MsgQuerySignsForEvidenceRequest<br/>to SignsFor Engine]
    MsgResp1 --> Client([Return to Client])
```

<figcaption markdown="span">
`verifyAction` flowchart
</figcaption>
</figure>

#### Explanation

1. **Initial Request**
   - A client sends a `MsgVerificationRequest` containing:
     - `data`: The original data (`Signable`) that was allegedly signed
     - `commitment`: The signature (`Commitment`) to verify
     - `externalIdentity`: The identity that supposedly made the signature
     - `useSignsFor`: Flag indicating whether to check signs-for relationships

2. **Guard Phase** (`verifyGuard`)
   - Validates that the incoming message is a proper verification request
   - Checks occur in the following order:
     - Verifies message type is `MsgVerificationRequest`
     - If validation fails, request is rejected without entering the action phase
     - On success, passes control to `verifyActionLabel`

3. **Action Phase** (`verifyAction`)
   - Processing branches based on the `useSignsFor` flag:

   - **Direct Verification Path** (useSignsFor = false)

     - Directly verifies the commitment using the configured verifier
     - Creates `MsgVerificationReply` with:
       - `result`: Boolean indicating if verification succeeded
       - `err`: None (or Some error message if verification failed)
     - Sends response immediately back to requester

   - **SignsFor Path** (useSignsFor = true)

     - Checks if there are existing pending requests for this identity
     - If this is the first request:
       - Stores request in pending requests map
       - Sends `MsgQuerySignsForEvidenceRequest` to SignsFor Engine
     - If there are existing requests:
       - Only stores new request in pending requests map
     - No immediate response is sent to client

4. **State Management**
   - For direct verification: No state changes
   - For signs-for verification:
     - Updates pendingRequests map in VerificationLocalState
     - Stores:
       - The requester's engine ID
       - The data to verify
       - The commitment to verify
     - Maintains these until signs-for evidence is received

!!! warning "Important Notes"

    - Multiple requests for the same identity are batched to avoid duplicate signs-for queries
    - The engine ensures exactly one signs-for query per identity is in flight at any time

### `signsForReplyAction` flowchart

<figure markdown>

```mermaid
flowchart TD
    Start([Client Request]) --> MsgReq[MsgVerificationRequest<br/>data: Signable<br/>commitment: Commitment<br/>externalIdentity: ExternalIdentity<br/>useSignsFor: Bool]

    subgraph Guard["verifyGuard"]
        MsgReq --> ValidType{Is message type<br/>VerificationRequest?}
        ValidType -->|No| Reject([Reject Request])
        ValidType -->|Yes| ActionEntry[Enter Action Phase]
    end

    ActionEntry --> Action

    subgraph Action["verifyAction"]
        direction TB
        SignsFor{useSignsFor<br/>flag?}
        SignsFor -->|No| DirectVerify[Verify using configured<br/>verifier]
        SignsFor -->|Yes| CheckPending{Existing requests<br/>for this identity?}

        CheckPending -->|Yes| StorePending[Add to pending<br/>request list]
        CheckPending -->|No| RequestSF[Send SignsFor<br/>evidence request]

        StorePending & RequestSF --> UpdateState[Update state with<br/>pending request]
        DirectVerify --> Response1[Prepare immediate response]
        UpdateState --> Response2[Prepare pending response]
    end

    Response1 --> MsgResp1[MsgVerificationReply<br/>result: Bool<br/>err: none]
    Response2 --> MsgResp2[MsgQuerySignsForEvidenceRequest<br/>to SignsFor Engine]

    MsgResp1 & MsgResp2 --> Client([Return to Client])
```

<figcaption markdown="span">
`signsForReplyAction` flowchart
</figcaption>
</figure>

#### Explanation

Let me provide a detailed explanation of the SignsFor Reply flow chart, following the style used for previous engines:

### SignsFor Reply Flow

1. **Initial Request**
   - A message arrives from the SignsFor Engine containing:
     - `externalIdentity`: The identity the evidence relates to
     - `evidence`: The signs-for relationships evidence
     - `err`: Any error that occurred during evidence gathering

2. **Guard Phase** (`signsForReplyGuard`)
   - Validates incoming messages through these checks:
     - Verifies message type is `MsgQuerySignsForEvidenceReply`
     - Verifies the message sender is the known SignsFor Engine address
     - If validation fails, request is rejected without entering action phase
     - On success, passes control to `signsForReplyActionLabel`

3. **Action Phase** (`signsForReplyAction`)
   - Processes the SignsFor evidence reply through these steps:
     - Checks map of pending requests for the given external identity
     - If no pending requests exist:
       - No action needed
       - No responses are generated
     - If pending requests exist:
       - Processes each pending request using the received evidence
       - For each request, verifies the commitment using both the verifier and the signs-for evidence
       - Generates verification responses for all pending requesters
       - Clears all pending requests for this identity from the state

4. **Response Generation**
   - For each pending requester:
     - Creates `MsgVerificationReply` containing:
       - `result`: Boolean indicating if verification succeeded
       - `err`: None (or Some error if verification failed)
   - All responses are sent back to their original requesters
   - Each response uses mailbox ID 0

!!! warning "Important Notes"

    - The engine processes all pending requests for an identity at once when evidence arrives
    - The state is cleaned up (pending requests removed) regardless of verification results
    - Each original requester gets their own individual response

## Action arguments

### `ReplyTo`

```juvix
type ReplyTo := mkReplyTo@{
  whoAsked : Option EngineID;
  mailbox : Option MailboxID
};
```

This action argument contains the address and mailbox ID of where the
response message should be sent.

???+ code "Arguments"

    `whoAsked`:
    : The engine ID of the requester.

    `mailbox`:
    : The mailbox ID where the response should be sent.

### `VerificationActionArgument`

<!-- --8<-- [start:VerificationActionArgument] -->
```juvix
type VerificationActionArgument :=
  | VerificationActionArgumentReplyTo ReplyTo
;
```
<!-- --8<-- [end:VerificationActionArgument] -->

### `VerificationActionArguments`

<!-- --8<-- [start:verification-action-arguments] -->
```juvix
VerificationActionArguments : Type := List VerificationActionArgument;
```
<!-- --8<-- [end:verification-action-arguments] -->

## Actions

??? code "Auxiliary Juvix code"

    ### `VerificationAction`

    ```juvix
    VerificationAction : Type :=
      Action
        VerificationCfg
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### `VerificationActionInput`

    ```juvix
    VerificationActionInput : Type :=
      ActionInput
        VerificationCfg
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationActionArguments
        Anoma.Msg;
    ```

    ### `VerificationActionEffect`

    ```juvix
    VerificationActionEffect : Type :=
      ActionEffect
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

    ### `VerificationActionExec`

    ```juvix
    VerificationActionExec : Type :=
      ActionExec
        VerificationCfg
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

#### `verifyAction`

Verify a commitment.

State update
: If `useSignsFor` is true, the state is updated to store pending requests. Otherwise, the state remains unchanged.

Messages to be sent
: If `useSignsFor` is false, a `ReplyVerification` message is sent back to the requester. If `useSignsFor` is true and it's the first request for this identity, a `QuerySignsForEvidenceRequest` is sent to the SignsFor Engine.

Engines to be spawned
: No engines are created by this action.

Timer updates
: No timers are set or cancelled.

```juvix
verifyAction
  (input : VerificationActionInput)
  : Option VerificationActionEffect :=
  let
    env := ActionInput.env input;
    cfg := ActionInput.cfg input;
    tt := ActionInput.trigger input;
    localState := EngineEnv.localState env
  in case getEngineMsgFromTimestampedTrigger tt of {
    | some emsg :=
      case emsg of {
        | mkEngineMsg@{msg := Anoma.MsgVerification (MsgVerificationRequest (mkRequestVerification data commitment externalIdentity useSignsFor))} :=
          case useSignsFor of {
            | false :=
              some mkActionEffect@{
                env := env;
                msgs := [
                  mkEngineMsg@{
                    sender := getEngineIDFromEngineCfg cfg;
                    target := EngineMsg.sender emsg;
                    mailbox := some 0;
                    msg := Anoma.MsgVerification (MsgVerificationReply (mkReplyVerification
                      (Verifier.verify
                        (VerificationCfg.verifier (EngineCfg.cfg cfg) Set.empty externalIdentity)
                        (VerificationCfg.backend (EngineCfg.cfg cfg))
                        data commitment)
                      none))
                  }
                ];
                timers := [];
                engines := []
              }
            | true :=
              let
                existingRequests := Map.lookup externalIdentity (VerificationLocalState.pendingRequests localState);
                newPendingList := case existingRequests of {
                  | some reqs := reqs ++ [mkPair (EngineMsg.sender emsg) (mkPair data commitment)]
                  | none := [mkPair (EngineMsg.sender emsg) (mkPair data commitment)]
                };
                newPendingRequests := Map.insert externalIdentity newPendingList (VerificationLocalState.pendingRequests localState);
                newLocalState := localState@VerificationLocalState{
                  pendingRequests := newPendingRequests
                };
                newEnv := env@EngineEnv{
                  localState := newLocalState
                }
              in some mkActionEffect@{
                env := newEnv;
                msgs := case existingRequests of {
                  | some _ := []
                  | none := [
                    mkEngineMsg@{
                      sender := getEngineIDFromEngineCfg cfg;
                      target := VerificationCfg.signsForEngineAddress (EngineCfg.cfg cfg);
                      mailbox := some 0;
                      msg := Anoma.MsgSignsFor (MsgQuerySignsForEvidenceRequest (mkRequestQuerySignsForEvidence externalIdentity))
                    }
                  ]
                };
                timers := [];
                engines := []
              }
          }
        | _ := none
      }
    | _ := none
  };
```

#### `signsForReplyAction`

Process a signs-for response and handle pending requests.

State update
: The state is updated to remove the processed pending requests for the given external identity.

Messages to be sent
: `ReplyVerification` messages are sent to all requesters who were waiting for this SignsFor evidence.

Engines to be spawned
: No engines are created by this action.

Timer updates
: No timers are set or cancelled.

```juvix
signsForReplyAction
  (input : VerificationActionInput)
  : Option VerificationActionEffect :=
  let
    env := ActionInput.env input;
    cfg := ActionInput.cfg input;
    tt := ActionInput.trigger input;
    localState := EngineEnv.localState env
  in case getEngineMsgFromTimestampedTrigger tt of {
    | some emsg :=
      case emsg of {
        | mkEngineMsg@{msg := Anoma.MsgSignsFor (MsgQuerySignsForEvidenceReply (mkReplyQuerySignsForEvidence externalIdentity evidence err))} :=
          case Map.lookup externalIdentity (VerificationLocalState.pendingRequests localState) of {
            | some reqs :=
              let
                newPendingRequests := Map.delete externalIdentity (VerificationLocalState.pendingRequests localState);
                newLocalState := localState@VerificationLocalState{
                  pendingRequests := newPendingRequests
                };
                newEnv := env@EngineEnv{
                  localState := newLocalState
                }
              in some mkActionEffect@{
                env := newEnv;
                msgs := map (\{req :=
                  let
                    whoAsked := fst req;
                    data := fst (snd req);
                    commitment := snd (snd req)
                  in mkEngineMsg@{
                    sender := getEngineIDFromEngineCfg cfg;
                    target := whoAsked;
                    mailbox := some 0;
                    msg := Anoma.MsgVerification (MsgVerificationReply (mkReplyVerification
                      (Verifier.verify
                        (VerificationCfg.verifier (EngineCfg.cfg cfg) evidence externalIdentity)
                        (VerificationCfg.backend (EngineCfg.cfg cfg))
                        data commitment)
                      none))
                  }}) reqs;
                timers := [];
                engines := []
              }
            | none := some mkActionEffect@{
              env := env;
              msgs := [];
              timers := [];
              engines := []
            }
          }
        | _ := none
      }
    | _ := none
  };
```

## Action Labels

### `verifyActionLabel`

```juvix
verifyActionLabel : VerificationActionExec := Seq [ verifyAction ];
```

### `signsForReplyActionLabel`

```juvix
signsForReplyActionLabel : VerificationActionExec := Seq [ signsForReplyAction ];
```

## Guards

??? code "Auxiliary Juvix code"

    ### `VerificationGuard`

    <!-- --8<-- [start:VerificationGuard] -->
    ```juvix
    VerificationGuard : Type :=
      Guard
        VerificationCfg
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:VerificationGuard] -->

    ### `VerificationGuardOutput`

    <!-- --8<-- [start:VerificationGuardOutput] -->
    ```juvix
    VerificationGuardOutput : Type :=
      GuardOutput
        VerificationCfg
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:VerificationGuardOutput] -->

    ### `VerificationGuardEval`

    <!-- --8<-- [start:VerificationGuardEval] -->
    ```juvix
    VerificationGuardEval : Type :=
      GuardEval
        VerificationCfg
        VerificationLocalState
        VerificationMailboxState
        VerificationTimerHandle
        VerificationActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:VerificationGuardEval] -->

#### `verifyGuard`

Condition
: Message type is `VerificationRequest`.

<!-- --8<-- [start:verifyGuard] -->
```juvix
verifyGuard
  (tt : TimestampedTrigger VerificationTimerHandle Anoma.Msg)
  (cfg : EngineCfg VerificationCfg)
  (env : VerificationEnv)
  : Option VerificationGuardOutput :=
  case getEngineMsgFromTimestampedTrigger tt of {
    | some mkEngineMsg@{
        msg := Anoma.MsgVerification (MsgVerificationRequest _);
      } :=
      some mkGuardOutput@{
        action := verifyActionLabel;
        args := []
      }
    | _ := none
  };
```
<!-- --8<-- [end:verifyGuard] -->

#### `signsForReplyGuard`

Condition
: Message is a signs-for response from the SignsFor engine.

<!-- --8<-- [start:signsForReplyGuard] -->
```juvix
signsForReplyGuard
  (tt : TimestampedTrigger VerificationTimerHandle Anoma.Msg)
  (cfg : EngineCfg VerificationCfg)
  (env : VerificationEnv)
  : Option VerificationGuardOutput :=
  case getEngineMsgFromTimestampedTrigger tt of {
    | some emsg :=
      case emsg of {
        | mkEngineMsg@{
            msg := Anoma.MsgSignsFor (MsgQuerySignsForEvidenceReply _);
            sender := sender
          } :=
          case isEqual (Ord.cmp sender (VerificationCfg.signsForEngineAddress (EngineCfg.cfg cfg))) of {
            | true := some mkGuardOutput@{
              action := signsForReplyActionLabel;
              args := []
            }
            | false := none
          }
        | _ := none
      }
    | none := none
  };
```
<!-- --8<-- [end:signsForReplyGuard] -->

## The Verification Behaviour

### `VerificationBehaviour`

<!-- --8<-- [start:VerificationBehaviour] -->
```juvix
VerificationBehaviour : Type :=
  EngineBehaviour
    VerificationCfg
    VerificationLocalState
    VerificationMailboxState
    VerificationTimerHandle
    VerificationActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:VerificationBehaviour] -->

### Instantiation

<!-- --8<-- [start:verificationBehaviour] -->
```juvix
verificationBehaviour : VerificationBehaviour :=
  mkEngineBehaviour@{
    guards := First [
      verifyGuard;
      signsForReplyGuard
    ]
  };
```
<!-- --8<-- [end:verificationBehaviour] -->

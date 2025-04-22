---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - decryption
  - behaviour
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.decryption_behaviour;

    import prelude open;
    import arch.node.types.messages open;
    import arch.system.identity.identity open;
    import arch.node.types.engine open;
    import arch.node.engines.decryption_config open;
    import arch.node.engines.decryption_environment open;
    import arch.node.engines.decryption_messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma as Anoma open;
    ```

# Decryption Behaviour

## Overview

The behavior of the Decryption Engine defines how it processes incoming
decryption requests and produces the corresponding decrypted outputs.

## Decryption Action Flowchart

### `decryptAction` flowchart

<figure markdown>

```mermaid
flowchart TD
  Start([Client Request]) --> MsgReq[MsgDecryptionRequest<br/>data: Ciphertext]

  subgraph Guard["decryptGuard (Message Validation)"]
      MsgReq --> ValidType{Is message type<br/>DecryptionRequest?}
      ValidType -->|No| Reject([Reject Request])
      ValidType -->|Yes| ActionEntry[Enter Action Phase]
  end

  ActionEntry --> Action

  subgraph Action["decryptAction (Processing)"]
      direction TB
      Decrypt[Attempt decryption<br/>using backend decryptor]
      Decrypt --> Success{Decryption<br/>Successful?}
      Success -->|Yes| GoodResp[Create Reply<br/>with plaintext]
      Success -->|No| ErrResp[Create Reply<br/>with error]
  end

  GoodResp --> Reply[MsgDecryptionReply<br/>commitment: Plaintext<br/>err: none]
  ErrResp --> ErrReply[MsgDecryptionReply<br/>commitment: empty<br/>err: Some error]

  Reply --> Client([Return to Client])
  ErrReply --> Client

  style Guard fill:#f0f7ff,stroke:#333,stroke-width:2px
  style Action fill:#fff7f0,stroke:#333,stroke-width:2px
```

<figcaption markdown="span">

`decryptAction` flowchart

</figcaption>
</figure>

#### Explanation

1. **Initial Request**
   - A client sends a `MsgDecryptionRequest` containing encrypted data (`Ciphertext`).
   - The ciphertext must be encrypted for the identity associated with this decryption engine.
   - Any metadata needed for decryption should be included in the ciphertext structure.

2. **Guard Phase** (`decryptGuard`)
   - Validates incoming message structure and type.
   - Validation steps:
     - Verifies message type is `MsgDecryptionRequest`.
     - If validation fails, request is rejected immediately.
     - On success, passes control to `decryptActionLabel`.

3. **Action Phase** (`decryptAction`)
   - Processes valid decryption requests through these steps:
     - Extracts the ciphertext from the request.
     - Retrieves the decryptor from the engine's configuration.
     - Attempts to decrypt using the backend decryptor.
     - Constructs appropriate response based on result.

4. **Reply Generation**
   - **Successful Case**
     - Creates `MsgDecryptionReply` with:
       - `data`: The decrypted plaintext.
       - `err`: None.
   - **Error Case**
     - In all error cases, returns `MsgDecryptionReply` with:
       - `data`: emptyByteString (zero-length byte string).
       - `err`: Some "Decryption Failed".

5. **Reply Delivery**
   - Reply is sent back to the original requester.
   - Uses mailbox 0 (default mailbox for responses).

---

!!! note

    The commitment engine is stateless - each request is handled .

## Action arguments

### `ReplyTo`

```juvix
type ReplyTo := mkReplyTo@{
  whoAsked : Option EngineID;
  mailbox : Option MailboxID;
};
```

This action argument contains the address and mailbox ID of where the
response message should be sent.

???+ code "Arguments"

    `whoAsked`:
    : is the address of the engine that sent the message.

    `mailbox`:
    : is the mailbox ID where the response message should be sent.

### `DecryptionActionArgument`

<!-- --8<-- [start:DecryptionActionArgument] -->
```juvix
type DecryptionActionArgument :=
  | DecryptionActionArgumentReplyTo ReplyTo
  ;
```
<!-- --8<-- [end:DecryptionActionArgument] -->

### `DecryptionActionArguments`

<!-- --8<-- [start:decryption-action-arguments] -->
```juvix
DecryptionActionArguments : Type := List DecryptionActionArgument;
```
<!-- --8<-- [end:decryption-action-arguments] -->

## Actions

??? code "Auxiliary Juvix code"



    ### `DecryptionAction`

    ```juvix
    DecryptionAction : Type :=
      Action
        DecryptionLocalCfg
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        DecryptionActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```



    ### `DecryptionActionInput`

    ```juvix
    DecryptionActionInput : Type :=
      ActionInput
        DecryptionLocalCfg
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        DecryptionActionArguments
        Anoma.Msg;
    ```



    ### `DecryptionActionEffect`

    ```juvix
    DecryptionActionEffect : Type :=
      ActionEffect
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```



    ### `DecryptionActionExec`

    ```juvix
    DecryptionActionExec : Type :=
      ActionExec
        DecryptionLocalCfg
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        DecryptionActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```

### `decryptAction`

Process a decryption request.

State update
: The state remains unchanged.

Messages to be sent
: A `ReplyDecryption` message is sent back to the requester.

Engines to be spawned
: No engine is created by this action.

Timer updates
: No timers are set or cancelled.

<!-- --8<-- [start:decryptAction] -->
```juvix
decryptAction
  (input : DecryptionActionInput)
  : Option DecryptionActionEffect :=
  let
    env := ActionInput.env input;
    cfg := ActionInput.cfg input;
    tt := ActionInput.trigger input;
  in
    case getEngineMsgFromTimestampedTrigger tt of {
    | some emsg :=
      case EngineMsg.msg emsg of {
      | Anoma.Msg.MsgDecryption (DecryptionMsg.Request request) :=
        let
          decryptedData :=
            Decryptor.decrypt
              (DecryptionLocalCfg.decryptor (EngineCfg.cfg cfg))
              (DecryptionLocalCfg.backend (EngineCfg.cfg cfg))
              (RequestDecryption.data request);
          responseMsg := case decryptedData of {
            | none := ReplyDecryption.mkReplyDecryption@{
                data := emptyByteString;
                err := some "Decryption Failed"
              }
            | some plaintext := ReplyDecryption.mkReplyDecryption@{
                data := plaintext;
                err := none
              }
          }
        in some ActionEffect.mkActionEffect@{
          env := env;
          msgs := [
            EngineMsg.mk@{
              sender := getEngineIDFromEngineCfg cfg;
              target := EngineMsg.sender emsg;
              mailbox := some 0;
              msg := Anoma.Msg.MsgDecryption (DecryptionMsg.Reply responseMsg)
            }
          ];
          timers := [];
          engines := []
        }
      | _ := none
      }
    | _ := none
    };
```
<!-- --8<-- [end:decryptAction] -->

## Action Labels

### `decryptActionLabel`

```juvix
decryptActionLabel : DecryptionActionExec := ActionExec.Seq [ decryptAction ];
```

## Guards

??? code "Auxiliary Juvix code"

    ### `DecryptionGuard`

    <!-- --8<-- [start:DecryptionGuard] -->
    ```juvix
    DecryptionGuard : Type :=
      Guard
        DecryptionLocalCfg
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        DecryptionActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:DecryptionGuard] -->

    ### `DecryptionGuardOutput`

    <!-- --8<-- [start:DecryptionGuardOutput] -->
    ```juvix
    DecryptionGuardOutput : Type :=
      GuardOutput
        DecryptionLocalCfg
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        DecryptionActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:DecryptionGuardOutput] -->



    ### `DecryptionGuardEval`

    <!-- --8<-- [start:DecryptionGuardEval] -->
    ```juvix
    DecryptionGuardEval : Type :=
      GuardEval
        DecryptionLocalCfg
        DecryptionLocalState
        DecryptionMailboxState
        DecryptionTimerHandle
        DecryptionActionArguments
        Anoma.Msg
        Anoma.Cfg
        Anoma.Env;
    ```
    <!-- --8<-- [end:DecryptionGuardEval] -->

### `decryptGuard`

Condition
: Message type is `MsgDecryptionRequest`.

<!-- --8<-- [start:decryptGuard] -->
```juvix
decryptGuard
  (tt : TimestampedTrigger DecryptionTimerHandle Anoma.Msg)
  (cfg : DecryptionCfg)
  (env : DecryptionEnv)
  : Option DecryptionGuardOutput :=
  case getEngineMsgFromTimestampedTrigger tt of {
    | some EngineMsg.mk@{
        msg := Anoma.Msg.MsgDecryption (DecryptionMsg.Request _);
      } := some GuardOutput.mkGuardOutput@{
        action := decryptActionLabel;
        args := []
      }
    | _ := none
  };
```
<!-- --8<-- [end:decryptGuard] -->

## The Decryption Behavior

### `DecryptionBehaviour`

<!-- --8<-- [start:DecryptionBehaviour] -->
```juvix
DecryptionBehaviour : Type :=
  EngineBehaviour
    DecryptionLocalCfg
    DecryptionLocalState
    DecryptionMailboxState
    DecryptionTimerHandle
    DecryptionActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:DecryptionBehaviour] -->

### Instantiation

<!-- --8<-- [start:decryptionBehaviour] -->
```juvix
decryptionBehaviour : DecryptionBehaviour :=
  EngineBehaviour.mk@{
    guards :=
      GuardEval.First [
        decryptGuard
      ];
  };
```
<!-- --8<-- [end:decryptionBehaviour] -->

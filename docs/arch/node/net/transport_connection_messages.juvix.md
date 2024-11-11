---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-connection-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.transport_connection_messages;

    import arch.node.net.transport_types open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import prelude open;
    ```

# Transport Connection Messages

These are the messages that the *Transport Connection* engine can receive.

## Message interface

### `MsgTransportConnectionSendMsg SendMsg

--8<-- [start:SendMsg]
Send a message to the remote node via the established connection.

```juvix
type SendMsg := mkSendMsg {
  msg : NodeMsg;
}
```
--8<-- [end:SendMsg]

### `MsgTransportConnection`

<!-- --8<-- [start:MsgTransportConnection] -->
```juvix
type MsgTransportConnection :=
  | MsgTransportConnectionSendMsg SendMsg
  ;
```
<!-- --8<-- [end:MsgTransportConnection] -->

## Sequence Diagrams

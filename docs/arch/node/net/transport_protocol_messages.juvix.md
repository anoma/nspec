---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-protocol-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.transport_protocol_messages;

    import arch.node.net.transport_types open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import prelude open;
    ```

# Transport Protocol Messages

These are the messages that the *Transport Protocol* engine can receive.

## Message interface

### `MsgTransportProtocolSendMsg SendMsg

--8<-- [start:SendMsg]
Send a message to a remote node via the given transport address.

The *Transport Protocol* engine
spawns a new *Transport Connection* engine instance for the connection,
if it does not exist yet,
and forwards the `NodeMsg` to it.

```juvix
type SendMsg := mkSendMsg {
  addr : TransportAddress;
  msg : NodeMsg;
}
```
--8<-- [end:SendMsg]

### `MsgTransportProtocol`

<!-- --8<-- [start:MsgTransportProtocol] -->
```juvix
type MsgTransportProtocol :=
  | MsgTransportProtocolSendMsg SendMsg
  ;
```
<!-- --8<-- [end:MsgTransportProtocol] -->

## Sequence Diagrams

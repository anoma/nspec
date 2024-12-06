---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-engine
- engine-messages
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.transport_messages;

    import arch.node.net.transport_types open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Transport Messages

These are the messages that the Transport engine can receive.

## Message interface

### `TransportMsgSend`

Send a message to a remote node via the given transport address.

The *Transport Protocol* engine forwards the given message
to the *Transport Protocol* engine
responsible for the protocol of the given transport address.

<!-- --8<-- [start:TransportOutMsg] -->
```juvix
type TransportOutMsg := mkTransportOutMsg {
  addr : TransportAddress;
  msg : ByteString;
}
```
<!-- --8<-- [end:TransporOutMsg] -->

### `MsgTransport`

<!-- --8<-- [start:TransportMsg] -->
```juvix
type TransportMsg :=
  | TransportMsgSend TransportOutMsg
  ;
```
<!-- --8<-- [end:TransportMsg] -->

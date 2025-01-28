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

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.transport_messages;

    import arch.node.types.transport open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Transport Messages

These are the messages that the Transport engine can receive.

## Message interface

--8<-- "./transport_messages.juvix.md:TransportMsg"

## Message types

---

### `TransportOutMsg`

Send a message to a remote node via the given transport address.

The *Transport Protocol* engine forwards the given message to the *Transport
Protocol* engine responsible for the protocol of the given transport address.

<!-- --8<-- [start:TransportOutMsg] -->
```juvix
type TransportOutMsg := mkTransportOutMsg {
  addr : TransportAddress;
  msg : ByteString;
}
```
<!-- --8<-- [end:TransporOutMsg] -->

### `TransportMsg`

<!-- --8<-- [start:TransportMsg] -->
```juvix
type TransportMsg :=
  | TransportMsgSend TransportOutMsg
  ;
```
<!-- --8<-- [end:TransportMsg] -->

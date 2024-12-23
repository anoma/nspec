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
    import arch.node.net.node_proxy_messages open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Transport Protocol Messages

These are the messages that the *Transport Protocol* engine can receive.

## Message interface

### `TransportProtocolMsgSend`

Send a message to a remote node via the given transport address.

The *Transport Protocol* engine
spawns a new *Transport Connection* engine instance for the connection
if it does not exist yet,
and forwards the given message to it.

<!-- --8<-- [start:TransportOutMsg] -->
```juvix
type TransportOutMsg := mkTransportOutMsg {
  addr : TransportAddress;
  prefs : TransportPrefs;
  expiry : Time;
  msg : NodeMsg;
}
```
<!-- --8<-- [end:TransportOutMsg] -->

???+ quote "Arguments"

    `addr`
    : Transport address.

    `msg`
    : Node message.

### `TransportProtocolMsg`

<!-- --8<-- [start:TransportProtocolMsg] -->
```juvix
type TransportProtocolMsg :=
  | TransportProtocolMsgSend TransportOutMsg
  ;
```
<!-- --8<-- [end:TransportProtocolMsg] -->
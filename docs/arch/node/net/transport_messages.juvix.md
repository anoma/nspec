---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.transport_messages;

    import arch.node.types.messages open;
    import prelude open;
    ```

# Transport Messages

These are the messages that the Transport engine can receive/respond to.

## Message interface

### `MsgTransportConnectRequest TransportConnectRequest`

--8<-- [start:MsgTransportConnectRequest]
Request to initiate a connection to a remote node over a specific transport protocol.

```juvix
type TransportConnectRequest := mkTransportConnectRequest {
  node : NodeID;
  proto : TransportProtocol;
  addr : TransportAddress;
  msg : EngineMsg;
}
```
--8<-- [end:MsgTransporConnectRequest]

### `MsgTransportConnectReply TransportConnectReply`

Reply to a `MsgTransportConnectRequest`.

#### `MsgTransportConnectReplyOk`

Connection successful.

```juvix
type TransportConnectReplyOk :=
  mkTransportConnectReplyOk {
    engine_name : EngineName;
  }
```

`engine_name`
: Engine instance name that handles the connection.

#### `MsgTransportConnectReplyError`

Connection failed.

```juvix
type TransportConnectReplyError :=
  | TransportConnectReplyErrorNoRoute
  | TransportConnectReplyErrorRefused
  | TransportConnectReplyErrorTimeout
  ;
```

`TransportConnectReplyErrorNoRoute`
: No route found.

`TransportConnectReplyErrorRefused`
: Connection refused.

`TransportConnectReplyErrorTimeout`
: Connection timeout

#### `TransportConnectReply`

```juvix
TransportConnectReply := Result TransportConnectReplyOk TransportConnectReplyError;
```

### `MsgTransport`

<!-- --8<-- [start:TemplateMsg] -->
```juvix
type MsgTransport :=
  | MsgTransportConnectRequest TransportConnectRequest
  | MsgTransportConnectReply TransportConnectReply
  ;
```
<!-- --8<-- [end:TemplateMsg] -->

## Sequence Diagrams

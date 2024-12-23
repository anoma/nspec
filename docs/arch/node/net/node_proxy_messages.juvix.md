---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- node-proxy-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.node_proxy_messages;

    import arch.node.net.router_types open;
    import arch.node.net.transport_types open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Node Proxy Messages

## Message interface

### `NodeProxyMsgSend`

Send an `EngineMsg` to the remote node
with the given transport preferences
and expiry time for send retries.

Sender: any local engine.

#### `NodeOutMsg`

Outgoing message to a remote node.

<!-- --8<-- [start:NodeOutMsg] -->
```juvix
type NodeOutMsg M := mkNodeOutMsg {
  prefs : TransportPrefs;
  expiry : Time;
  msg : EngineMsg M;
};
```
<!-- --8<-- [end:NodeOutMsg] -->

### `NodeProxyMsgRecv`

Receive a message from the remote node.

#### `NodeMsg`

A message sent between nodes.

<!-- --8<-- [start:NodeMsg] -->
```juvix
type NodeMsg := mkNodeMsg {
  seq : Nat;
  msg : EncryptedMsg;
};
```
<!-- --8<-- [end:NodeMsg] -->

???+ quote "Arguments"

    `seq`
    Message sequence number of the sender.

    `msg`
    Encrypted `SerializedMsg` message that contains an `EngineMsg`.

### `NodeProxyMsgConnectRequest ConnectRequest`

Request a connection to a remote node.

The responder may accept or deny the request.
As part of the connection establishment,
first a protocol version negotiation takes place.
the highest common supported protocol version is chosen,
or else the connection fails.

Nodes let each other know about their own latest `NodeAdvert` version,
and the version they know of from the other party,
and if necessary, send each other an updated `NodeAdvert`
after the connection is established.

```juvix
type ConnectRequest :=
  mkConnectRequest {
    proto_ver_min : Nat;
    proto_ver_max : Nat;
    src_node_id : NodeID;
    dst_node_id : NodeID;
    src_node_advert_ver : Nat;
    dst_node_advert_ver : Nat;
  }
```

`proto_ver_min`
: Min. supported protocol version range.

`proto_ver_max`
: Max. supported protocol version range.

`src_node_id`
: Source node ID.

`dst_node_id`
: Destination node ID.

`src_node_advert_ver`
: Latest `NodeAdvert` version of the source node.

`dst_node_advert_ver`
: Latest known `NodeAdvert` version of the destination node.

### `NodeProxyMsgConnectReply`

Reply to a `NodeProxyMsgConnectRequest`.

#### `NodeProxyMsgConnectReplyOk`

Accept a connection from a node.

```juvix
type ConnectReplyOk :=
  mkConnectReplyOk {
    proto_ver : Nat;
    node_advert_ver : Pair Nat Nat;
  }
```

`proto_ver`
: Protocol version to use.

`node_advert_ver`
: Latest local `NodeAdvert` version.

#### `NodeProxyMsgConnectReplyError`

Refuse a connection from a node.

```juvix
type ConnectReplyError :=
  | ConnectReplyErrorOverCapacity
  | ConnectReplyErrorIncompatible
  | ConnectReplyErrorDenied
  ;
```

`NodeConnectReplyErrorOverCapacity`
: Node over capacity. Temporary failure.

`NodeConnectReplyErrorIncompatible`
: Incompatible protocol versions.

`NodeConnectReplyErrorDenied`
: Connection denied by local policy.

#### `ConnectReply`

```juvix
ConnectReply : Type := Result ConnectReplyOk ConnectReplyError;
```

### `NodeProxyMsgNodeAdvert NodeAdvert`

Node advertisement update from the remote node.
The *Node Proxy* forwards this to the router.

--8<-- "./router_types.juvix.md:NodeAdvert"

### `NodeProxyMsgNodeAdvertReply`

### `NodeProxyMsgSetPermanence ConnectionPermanence`

Set connection permanence to either ephemeral or permanent.

```juvix
type ConnectionPermanence :=
  | NodeProxyMsgConnectionEphemeral
  | NodeProxyMsgConnectionPermanent
  ;
```

## `NodeProxyMsg`

All *Node Proxy* engine messages.

```juvix
type NodeProxyMsg M :=
  | NodeProxyMsgSend (NodeOutMsg M)
  | NodeProxyMsgRecv NodeMsg
  | NodeProxyMsgConnectRequest ConnectRequest
  | NodeProxyMsgConnectReply ConnectReply
  | NodeProxyMsgNodeAdvert NodeAdvert
  | NodeProxyMsgSetPermanence ConnectionPermanence
  ;
```

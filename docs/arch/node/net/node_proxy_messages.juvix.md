??? quote "Juvix imports"

    ```juvix
    module arch.node.net.node_proxy_messages;

    import arch.node.net.router_types open;
    import arch.node.net.transport_types open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import prelude open;
    ```

# Node Proxy Messages

## Message interface

### `MsgNodeProxySendMsg SendMsg`

--8<-- [start:SendMsg]
Send an `EngineMsg` to a remote node
with the given transport preferences
and expiry time for send retries.

```juvix
type SendMsg M := mkSendMsg {
  tprefs : TransportPrefs;
  expiry : Time;
  msg : EngineMsg M;
};
```
--8<-- [end:EngineMsg]

### `MsgNodeProxyNodeMsg NodeMsg`

--8<-- [start:NodeMsg]
A message sent between nodes.

```juvix
type NodeMsg M := mkNodeMsg {
  seq : Nat;
  msg : EngineMsg M;
};
```
--8<-- [end:NodeMsg]

`seq`
Sequence number of the sender.

### `MsgNodeProxyConnectRequest NodeConnectRequest`

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
type NodeConnectRequest :=
  mkNodeConnectRequest {
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

### `MsgNodeProxyConnectReply NodeConnectReply`

Reply to a `MsgNodeProxyConnectRequest`.

#### `MsgNodeProxyConnectReplyOk`

Accept a connection from a node.

```juvix
type NodeConnectReplyOk :=
  mkNodeConnectReplyOk {
    proto_ver : Nat;
    node_advert_ver : Pair Nat Nat;
  }
```

`proto_ver`
: Protocol version to use.

`node_advert_ver`
: Latest local `NodeAdvert` version.

#### `MsgNodeProxyConnectReplyError`

Refuse a connection from a node.

```juvix
type NodeConnectReplyError :=
  | NodeConnectReplyErrorOverCapacity
  | NodeConnectReplyErrorIncompatible
  | NodeConnectReplyErrorDenied
  ;
```

`NodeConnectReplyErrorOverCapacity`
: Node over capacity. Temporary failure.

`NodeConnectReplyErrorIncompatible`
: Incompatible protocol versions.

`NodeConnectReplyErrorDenied`
: Connection denied by local policy.

#### `NodeConnectReply`

```juvix
NodeConnectReply : Type := Result NodeConnectReplyOk NodeConnectReplyError;
```

### `MsgNodeProxyNodeAdvert NodeAdvert`

Node advertisement update from the remote node.
The *Node Proxy* forwards this to the router.

--8<-- "./router_types.juvix.md:NodeAdvert"

### `MsgNodeProxyNodeAdvertReply`

### `MsgNodeProxySetPermanence ConnectionPermanence`

Set connection permanence to either ephemeral or permanent.

```juvix
type ConnectionPermanence M :=
  | MsgNodeProxyConnectionEphemeral
  | MsgNodeProxyConnectionPermanent
  ;
```

## `MsgNodeProxy`

All *Node Proxy* engine messages.

```juvix
type MsgNodeProxy M :=
  | MsgNodeProxySendMsg (SendMsg M)
  | MsgNodeProxyNodeMsg (NodeMsg M)
  | MsgNodeProxyConnectRequest NodeConnectRequest
  | MsgNodeProxyConnectReply NodeConnectReply
  | MsgNodeProxyNodeAdvert NodeAdvert
  | MsgNodeProxySetPermanence ConnectionPermanence
  ;
```

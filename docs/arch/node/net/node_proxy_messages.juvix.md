??? quote "Juvix imports"

    ```juvix
    module arch.node.net.node_proxy_messages;

    import arch.node.net.router_types open;
    import arch.node.net.transport_types open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import prelude open public;
    ```

# Node Proxy Messages

## Message interface

### `MsgNodeProxyNodeMsg NodeMsg`

--8<-- [start:NodeMsg]
An outgoing unicast message sent to a remote node:
consists of the destination node identity,
along with transport preferences,
expiry time for send retries,
and the engine message.

```juvix
type NodeMsg M := mkNodeMsg {
  dst : Option NodeID;
  tprefs : TransportPrefs;
  expiry : Time;
  msg : EngineMsg M;
};
```
--8<-- [end:NodeMsg]

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
NodeConnectReply := Result NodeConnectReplyOk NodeConnectReplyError;
```

### `MsgNodeProxyNodeAdvert NodeAdvert`

Node advertisement update.

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
  | MsgNodeProxyNodeMsg (NodeMsg M)
  | MsgNodeProxyConnectRequest NodeConnectRequest
  | MsgNodeProxyConnectReply NodeConnectReply
  | MsgNodeProxyNodeAdvert NodeAdvert
  | MsgNodeProxySetPermanence ConnectionPermanence
  ;
```

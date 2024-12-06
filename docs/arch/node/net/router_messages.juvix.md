---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- router-engine
- engine-messages
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.router_messages;

    import arch.node.net.router_types open;
    import arch.node.net.transport_types open;
    import arch.node.net.node_proxy_messages open;
    import arch.node.net.pub_sub_topic_messages open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Router Messages

## Message interface

### `RouterMsgNodeSend`

Send a message to a [[Node Proxy]].
If it does not exist yet, the *Router* spawns a new instance beforehand.

--8<-- "./node_proxy_messages.juvix.md:NodeOutMsg"

### `RouterMsgTopicForward`

Forward a `TopicMsg` to the corresponding [[Pub/Sub Topic]].
If the topic does not exist, the message is dropped.
This happens when there are no subscribers.

--8<-- "./topic_messages.juvix.md:TopicMsg"

### `RouterMsgNodeConnectRequest`

Request to establish a connection to a remote node.

The *Router* spawns a new [[Node Proxy]] if it does not exist yet,
and sets the connection permanence of the [[Node Proxy]]
via `MsgNodeProxySetPermanence`.

<!-- --8<-- [start:NodeConnectRequest] -->
```juvix
type NodeConnectRequest :=
  mkNodeConnectRequest {
    node_id : NodeID;
    permanent : Bool;
  }
```
<!-- --8<-- [end:NodeConnectRequest] -->

???+ quote "Arguments"

    `node_id`
    : Node ID to connect to.

    `permanent`
    : Whether or not the connection should be permanent.

### `NodeConnectReply`

Reply to a `NodeConnectRequest`.

#### `NodeConnectReplyOk`

Example OK reply.

<!-- --8<-- [start:NodeConnectReplyOk] -->
```juvix
type NodeConnectReplyOk : Type :=
  mkExampleReplyOk {
    argOne : Nat;
  }
```
<!-- --8<-- [end:NodeConnectReplyOk] -->

???+ quote "Arguments"

    `argOne`
    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

#### `NodeConnectReplyError`

Example error reply.

<!-- --8<-- [start:NodeConnectReplyError] -->
```juvix
type NodeConnectReplyError : Type :=
  | NodeConnectReplyErrorUnknown
  | NodeConnectReplyErrorDenied
  ;
```
<!-- --8<-- [end:NodeConnectReplyError] -->

???+ quote "Error types"

    `NodeConnectReplyErrorUnknown`
    : No `NodeAdvert` known for node.

    `NodeConnectReplyErrorDenied`
    : Connection to node denied by local policy.

#### `NodeConnectReply`

<!-- --8<-- [start:NodeConnectReply] -->
```juvix
NodeConnectReply : Type := Result NodeConnectReplyError NodeConnectReplyOk;
```
<!-- --8<-- [end:NodeConnectReply] -->

### `RouterMsgTopicSub TopicSub`

Allow local engines to subscribe to a [[Pub/Sub Topic]]
if a `TopicAdvert` is known for the topic.

The *Router* forwards the `TopicSub` message to the [[Pub/Sub Topic]]
engine instance responsible for the topic.
If necessary, it spawns a new [[Pub/Sub Topic]] engine instance beforehand.

```juvix
type RouterSub :=
  mkRouterSub {
    topic_id : TopicID;
  }
```

`topic_id`
: Topic ID.

### `RouterMsgTopicUnsub TopicUnsub`

Allow local engines to unsubscribe from a [[Pub/Sub Topic]]
if the topic exists.

The *Router* forwards the `TopicUnsub` message to the [[Pub/Sub Topic]].

```juvix
type RouterTopicUnsub :=
  mkRouterTopicsub {
    topic_id : TopicID;
  }
```

`topic_id`
: Topic ID.

## `RouterMsgNodeAdvert NodeAdvert`

Node advertisement update.

--8<-- "./router_types.juvix.md:NodeAdvert"

## `RouterMsgTopicAdvert TopicAdvert`

Topic advertisement update.

--8<-- "./router_types.juvix.md:TopicAdvert"

## `RouterMsg`

All *Router* engine messages.

```juvix
type RouterMsg M :=
  | RouterMsgNodeSend (NodeOutMsg M)
  | RouterMsgTopicForward TopicMsg
  | RouterMsgNodeConnectRequest NodeConnectRequest
  | RouterMsgNodeAdvert NodeAdvert
  | RouterMsgTopicAdvert TopicAdvert
  ;
```

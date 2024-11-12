??? quote "Juvix imports"

    ```juvix
    module arch.node.net.router_messages;

    import arch.node.net.router_types open;
    import arch.node.net.transport_types open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import prelude open;
    ```

# Router Messages

## Message interface

### `MsgRouterEngineMsg EnigneMsg`

Forward a message to a local engine.

--8<-- "../types/messages.juvix.md:EngineMsg"`

### `MsgRouterNodeMsg SendMsg`

Send a message to a [[Node Proxy]].
If it does not exist yet, the *Router* spawns a new instance beforehand.

--8<-- "./node_proxy_messages:SendMsg"

### `MsgRouterTopicMsg TopicMsg`

Forward a `TopicMsg` to the corresponding pub/sub [[Topic]].
If the topic does not exist, the message is dropped.
This happens when there are no subscribers.

--8<-- "./topic_messages:TopicMsg"

### `MsgRouterNodeConnect RouterNodeConnect`

Request to establish a permanent connection to a remote node.

The *Router* spawns a new [[Node Proxy]] if it does not exist yet,
or sets the connection permanence of an existing [[Node Proxy]]
via `MsgNodeProxySetPermanence`.

```juvix
type RouterNodeConnect :=
  mkRouterNodeConnect {
    node_id : NodeID;
  }
```

`node_id`
: Node ID to connect to.

### `MsgRouterTopicSub TopicSub`

Allow local engines to subscribe to a [[PubSub Topic]]
if a `TopicAdvert` is known for the topic.

The *Router* forwards the `TopicSub` message to the [[PubSub Topic]]
engine instance responsible for the topic.
If necessary, it spawns a new [[PubSub Topic]] engine instance beforehand.

```juvix
type RouterSub :=
  mkRouterSub {
    topic_id : TopicID;
  }
```

`topic_id`
: Topic ID.

### `MsgRouterTopicUnsub TopicUnsub`

Allow local engines to unsubscribe from a [[PubSub Topic]]
if the topic exists.

The *Router* forwards the `TopicUnsub` message to the [[PubSub Topic]].

```juvix
type RouterTopicUnsub :=
  mkRouterTopicsub {
    topic_id : TopicID;
  }
```

`topic_id`
: Topic ID.

## `MsgRouterNodeAdvert NodeAdvert`

Node advertisement update.

--8<-- "./router_types.juvix.md:NodeAdvert"

## `MsgRouterTopicAdvert TopicAdvert`

Topic advertisement update.

--8<-- "./router_types.juvix.md:TopicAdvert"

## `MsgRouter`

All *Router* engine messages.

```juvix
type MsgRouter M :=
  | MsgRouterEngineMsg (EngineMsg M)
  | MsgRouterNodeMsg (NodeMsg M)
  | MsgRouterTopicMsg TopicMsg
  | MsgRouterNodeConnect RouterNodeConnect
  | MsgRouterNodeAdvert NodeAdvert
  | MsgRouterTopicAdvert TopicAdvert
  ;
```

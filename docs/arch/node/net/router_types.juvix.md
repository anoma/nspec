# Router Types

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.router_types;

    import arch.node.net.transport_types open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    ```

## `NodeAdvert`

A self-signed *node advertisement* contains the node's
cryptographic identity and transport addresses.

```juvix
type NodeAdvert :=
  mkNodeAdvert {
    id : NodeID;
    addrs : List TransportAddress;
    version : Nat;
    created : AbsTime;
    sig : Commitment;
  };
```

`id`
: Node identity.

`addrs`
: Transport addresses with preferences expressed as weights.

`version`
: Version number (incremented at every change).

`created`
: Time of creation.

`sig`
: Signature by `id`.

## `TopicAdvert`

A *topic advertisement* signed by the topic creator
contains the topic's cryptographic identity,
and the `NodeID` of a set of relay nodes
that can be used to subscribe to the topic.
These may be publishers, subscribers, or dedicated relay nodes for the topic.

```juvix
type TopicAdvert :=
  mkTopicAdvert {
    id : TopicID;
    relays : List NodeID;
    tags : List String;
    version : Nat;
    created : AbsTime;
    sig : Commitment;
  };
```

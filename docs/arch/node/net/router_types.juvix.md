# Router Types

??? quote "Juvix preamble"

    ```juvix
    module arch.node.net.router_types;

    import arch.node.net.transport_types open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import prelude open;
    ```

## `NodeAdvert`

A self-signed *node advertisement* contains the node's
cryptographic identity, transport addresses,
and prekeys for asynchronous encrypted communication.

```juvix
type NodeAdvert :=
  mkNodeAdvert {
    id : NodeID; 
    addrs : List TransportAddress;
    prekeys : List ExternalID;
    version : Nat;
    created : AbsTime;
    sig : Commitment;
  };
```

`id`
: Node identity.

`addrs`
: Transport addresses with preferences expressed as weights.

`prekeys`
: Prekeys for asynchronous communication.

`version`
: Version number (incremented at every change).

`created`
: Time of creation.

`prekeys`
: Prekeys for initiating asynchronous Diffie-Hellman handshake with the node.

`sig`
: Signature by `id`.

## `TopicAdvert`

A self-signed *node advertisement* contains the node's
cryptographic identity, transport addresses,
and prekeys for asynchronous encrypted communication.

```juvix
type NodeAdvert :=
  mkNodeAdvert {
    id : NodeID; 
    addrs : List TransportAddress;
    prekeys : List ExternalID;
    version : Nat;
    created : AbsTime;
    sig : Commitment;
  };
```

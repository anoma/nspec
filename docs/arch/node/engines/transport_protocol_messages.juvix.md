---
icon: material/message-draw
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - transport
  - message-types
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.transport_protocol_messages;

    import arch.node.types.transport open;
    import arch.node.engines.router_messages open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Transport Protocol Messages

These are the messages that the *Transport Protocol* engine can receive.

## Message interface

--8<-- "./transport_protocol_messages.juvix.md:TransportProtocolMsg"

## Message types

### `TransportOutMsg`

Send a message to a remote node via the given transport address.

The *Transport Protocol* engine spawns a new *Transport Connection* engine
instance for the connection if it does not exist yet,
and forwards the given message to it.

<!-- --8<-- [start:TransportOutMsg] -->
```juvix
type TransportOutMsg := mkTransportOutMsg@{
  addr : TransportAddress;
  prefs : TransportPrefs;
  expiry : Time;
  msg : NodeMsg;
}
```
<!-- --8<-- [end:TransportOutMsg] -->

???+ code "Arguments"

    `addr`
    : Transport address.

    `prefs`
    : Transport preferences.

    `expiry`
    : Expiry time for send retries.

    `msg`
    : Node message.

### `TransportProtocolMsg`

<!-- --8<-- [start:TransportProtocolMsg] -->
```juvix
type TransportProtocolMsg :=
  | Send TransportOutMsg
  ;
```
<!-- --8<-- [end:TransportProtocolMsg] -->

## Engine components

- [[Transport Protocol Configuration]]
- [[Transport Protocol Environment]]
- [[Transport Protocol Behaviour]]

---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-connection-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.transport_connection_messages;

    import arch.node.engines.transport_types open;
    import arch.node.engines.router_messages open;

    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Transport Connection Messages

These are the messages that the *Transport Connection* engine can receive.

## Message interface

### `TransportConnectionMsgSend`

Send a message to the remote node via the established connection.

<!-- --8<-- [start:TransportConnectionOutMsg] -->
```juvix
type TransportConnectionOutMsg := mkTransportConnectionOutMsg {
  expiry : Time;
  msg : NodeMsg;
}
```
<!-- --8<-- [end:TransportConnectionOutMsg] -->

### `TransportConnectionMsg`

<!-- --8<-- [start:TransportConnectionMsg] -->
```juvix
type TransportConnectionMsg :=
  | TransportConnectionMsgSend TransportConnectionOutMsg
  ;
```
<!-- --8<-- [end:TransportConnectionMsg] -->

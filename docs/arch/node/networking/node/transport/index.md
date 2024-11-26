---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Transport

## Overview

### Purpose

<!-- --8<-- [start:purpose] -->
The [[Transport#transport]] engine is responsible for
sending and receiving messages from other nodes over the network,
establishing and maintaining authenticated and encrypted communication channels
to other nodes via various transport protocols.
<!-- --8<-- [end:purpose] -->

## State

The *Transport* engine maintains a [[ConnectionPool#connectionpool]],
a *pool of open connections* associated with [[NodeIdentity#nodeidentity|node identities]]
of connected nodes.
For protocols that support session resumption (such as QUIC, TLS),
it also maintains a [[TransportSessionCache#transportsessioncache]] for this purpose.

## Messages received

### [[P2PMessage to Transport#p2pmessage-transport|P2PMessage]]

--8<-- "transport/messages/p2p_message.md:purpose"

--8<-- "transport/messages/p2p_message.md:type"

### [[TransportMessage#transportmessage]]

--8<-- "transport/messages/transport_message.md:purpose"

--8<-- "transport/messages/transport_message.md:type"

### [[ConnectRequest#connectrequest]]

--8<-- "transport/messages/connect_request.md:purpose"

--8<-- "transport/messages/connect_request.md:type"

### [[DisconnectRequest#disconnectrequest]]

--8<-- "transport/messages/disconnect_request.md:purpose"

--8<-- "transport/messages/disconnect_request.md:type"

### [[ConnectedNodesRequest#connectednodesrequest]]

--8<-- "transport/messages/connected_nodes_request.md:purpose"

--8<-- "transport/messages/connected_nodes_request.md:type"

## Notifications sent

### [[NodeConnected#nodeconnected]]

--8<-- "transport/notifications/node_connected.md:purpose"

--8<-- "transport/notifications/node_connected.md:type"

### [[NodeConnectFailed#nodeconnectfailed]]

--8<-- "transport/notifications/node_disconnected.md:purpose"

--8<-- "transport/notifications/node_disconnected.md:type"

### [[NodeDisconnected#nodedisconnected]]

--8<-- "transport/notifications/node_connect_failed.md:purpose"

--8<-- "transport/notifications/node_connect_failed.md:type"

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

--8<-- "transport/messages/transport_message.md:sequence"

--8<-- "transport/messages/connect_request.md:sequence"

--8<-- "transport/messages/disconnect_request.md:sequence"

--8<-- "transport/messages/connected_nodes_request.md:sequence"

--8<-- "transport/notifications/node_connected.md:sequence"

--8<-- "transport/notifications/node_disconnected.md:sequence"

--8<-- "transport/notifications/node_connect_failed.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>

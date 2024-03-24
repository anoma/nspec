<div class="engine">

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

{{#include transport/messages/p2p-message.md:purpose}}

{{#include transport/messages/p2p-message.md:type}}

### [[TransportMessage#transportmessage]]

{{#include transport/messages/transport-message.md:purpose}}

{{#include transport/messages/transport-message.md:type}}

### [[ConnectRequest#connectrequest]]

{{#include transport/messages/connect-request.md:purpose}}

{{#include transport/messages/connect-request.md:type}}

### [[DisconnectRequest#disconnectrequest]]

{{#include transport/messages/disconnect-request.md:purpose}}

{{#include transport/messages/disconnect-request.md:type}}

### [[ConnectedNodesRequest#connectednodesrequest]]

{{#include transport/messages/connected-nodes-request.md:purpose}}

{{#include transport/messages/connected-nodes-request.md:type}}

## Notifications sent

### [[NodeConnected#nodeconnected]]

{{#include transport/notifications/node-connected.md:purpose}}

{{#include transport/notifications/node-connected.md:type}}

### [[NodeConnectFailed#nodeconnectfailed]]

{{#include transport/notifications/node-disconnected.md:purpose}}

{{#include transport/notifications/node-disconnected.md:type}}

### [[NodeDisconnected#nodedisconnected]]

{{#include transport/notifications/node-connect-failed.md:purpose}}

{{#include transport/notifications/node-connect-failed.md:type}}

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

{{#include transport/messages/transport-message.md:sequence}}

{{#include transport/messages/connect-request.md:sequence}}

{{#include transport/messages/disconnect-request.md:sequence}}

{{#include transport/messages/connected-nodes-request.md:sequence}}

{{#include transport/notifications/node-connected.md:sequence}}

{{#include transport/notifications/node-disconnected.md:sequence}}

{{#include transport/notifications/node-connect-failed.md:sequence}}
```
<!-- --8<-- [end:messages] -->

</div>

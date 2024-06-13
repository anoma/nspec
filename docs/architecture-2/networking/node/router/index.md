---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Router

## Overview

### Purpose

<!-- --8<-- [start:purpose] -->
The [[Router#router]] is responsible for forwarding both intra-node and inter-node messages between engine instances.
It forwards intra-node messages directly between local engines,
and sends and receives inter-node messages via the [[Transport#transport]] engine.
It makes routing decisions based on the [[DestinationIdentity#destinationidentity]] in [[EngineMessage#enginemessage]] headers,
and retrieves routing information for identities from the [[Network Identity Store#network-identity-store]] engine.
<!-- --8<-- [end:purpose] -->

## State

### [[RoutingTable#routingtable]]

--8<-- "router/types/routing-table.md:purpose"

--8<-- "router/types/routing-table.md:type"

## Messages received

### [[EngineMessage#enginemessage]]

--8<-- "router/messages/engine-message.md:purpose"

--8<-- "router/messages/engine-message.md:type"

### [[P2PMessage#p2pmessage]]

--8<-- "router/messages/p2p-message.md:purpose"

--8<-- "router/messages/p2p-message.md:type"

### [[RelayMessage#relaymessage]]

--8<-- "router/messages/relay-message.md:purpose"

--8<-- "router/messages/relay-message.md:type"

### [[TopicCreateRequest#topiccreaterequest]]

--8<-- "router/messages/topic-create-request.md:purpose"

--8<-- "router/messages/topic-create-request.md:type"

### [[TopicDeleteRequest#topicdeleteRequest]]

--8<-- "router/messages/topic-delete-request.md:purpose"

--8<-- "router/messages/topic-delete-request.md:type"

### [[TopicSubRequest#topicsubrequest]]

--8<-- "router/messages/topic-sub-request.md:purpose"

--8<-- "router/messages/topic-sub-request.md:type"

### [[TopicUnsubRequest#topicunsubrequest]]

--8<-- "router/messages/topic-unsub-request.md:purpose"

--8<-- "router/messages/topic-unsub-request.md:type"

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

--8<-- "router/messages/engine-message.md:sequence"

--8<-- "router/messages/p2p-message.md:sequence"

--8<-- "router/messages/relay-message.md:sequence"

--8<-- "router/messages/topic-create-request.md:sequence"

--8<-- "router/messages/topic-delete-request.md:sequence"

--8<-- "router/messages/topic-sub-request.md:sequence"

--8<-- "router/messages/topic-unsub-request.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>

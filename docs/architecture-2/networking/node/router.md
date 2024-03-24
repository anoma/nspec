<div class="engine">

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

{{#include router/types/routing-table.md:purpose}}

{{#include router/types/routing-table.md:type}}

## Messages received

### [[EngineMessage#enginemessage]]

{{#include router/messages/engine-message.md:purpose}}

{{#include router/messages/engine-message.md:type}}

### [[P2PMessage#p2pmessage]]

{{#include router/messages/p2p-message.md:purpose}}

{{#include router/messages/p2p-message.md:type}}

### [[RelayMessage#relaymessage]]

{{#include router/messages/relay-message.md:purpose}}

{{#include router/messages/relay-message.md:type}}

### [[TopicCreateRequest#topiccreaterequest]]

{{#include router/messages/topic-create-request.md:purpose}}

{{#include router/messages/topic-create-request.md:type}}

### [[TopicDeleteRequest#topicdeleteRequest]]

{{#include router/messages/topic-delete-request.md:purpose}}

{{#include router/messages/topic-delete-request.md:type}}

### [[TopicSubRequest#topicsubrequest]]

{{#include router/messages/topic-sub-request.md:purpose}}

{{#include router/messages/topic-sub-request.md:type}}

### [[TopicUnsubRequest#topicunsubrequest]]

{{#include router/messages/topic-unsub-request.md:purpose}}

{{#include router/messages/topic-unsub-request.md:type}}

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

{{#include router/messages/engine-message.md:sequence}}

{{#include router/messages/p2p-message.md:sequence}}

{{#include router/messages/relay-message.md:sequence}}

{{#include router/messages/topic-create-request.md:sequence}}

{{#include router/messages/topic-delete-request.md:sequence}}

{{#include router/messages/topic-sub-request.md:sequence}}

{{#include router/messages/topic-unsub-request.md:sequence}}
```
<!-- --8<-- [end:messages] -->

</div>

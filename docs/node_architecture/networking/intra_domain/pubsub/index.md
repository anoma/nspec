---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# PubSub

## Purpose

The *Publish-Subscribe* *(PubSub)* engine implements a peer-to-peer topic-based publish-subscribe protocol.
It is responsible for handling P2P protocol messages and managing subscriptions.
Local engines send and receive pub/sub messages via the *[[Router#router]]*.

## ~Usage~

The *[[Router#router]]* engine interfaces with the *PubSub* engine directly,
while other local engines use the *Router*
to subscribe to topics and send messages destined to the multicast address of a pub/sub topic,
which the *Router* then forwards to *PubSub* for delivery.

## State

## [[PubSubRoutingTable#pubsubroutingtable]]

--8<-- "pubsub/types/pubsub_routing_table.md:purpose"

## Messages received

### [[TopicAdvert#topicadvert]]

--8<-- "pubsub/messages/topic_advert.md:purpose"

--8<-- "pubsub/messages/topic_advert.md:type"

### [[Subscribe#subscribe]]

--8<-- "pubsub/messages/subscribe.md:purpose"

--8<-- "pubsub/messages/subscribe.md:type"

### [[Unsubscribe#unsubscribe]]

--8<-- "pubsub/messages/unsubscribe.md:purpose"

--8<-- "pubsub/messages/unsubscribe.md:type"

### [[Event#event]]

--8<-- "pubsub/messages/event.md:purpose"

--8<-- "pubsub/messages/event.md:type"

### [[EngineMessage to PubSub#enginemessage-pubsub|EngineMessage]]

--8<-- "pubsub/messages/engine_message.md:purpose"

--8<-- "pubsub/messages/engine_message.md:type"

### [[SubscribeRequest#subscriberequest]]

--8<-- "pubsub/messages/subscribe_request.md:purpose"

--8<-- "pubsub/messages/subscribe_request.md:type"

### [[UnsubscribeRequest#unsubscriberequest]]

--8<-- "pubsub/messages/unsubscribe_request.md:purpose"

--8<-- "pubsub/messages/unsubscribe_request.md:type"

### [[StartAdvertRequest#subscriberequest]]

--8<-- "pubsub/messages/start_advert_request.md:purpose"

--8<-- "pubsub/messages/start_advert_request.md:type"

### [[StopAdvertRequest#subscriberequest]]

--8<-- "pubsub/messages/stop_advert_request.md:purpose"

--8<-- "pubsub/messages/stop_advert_request.md:type"

## Notifications sent

### [[TopicSubscribed#topicsubscribed]]

--8<-- "pubsub/notifications/topic_subscribed.md:purpose"

--8<-- "pubsub/notifications/topic_subscribed.md:type"

### [[TopicUnsubscribed#topicunsubscribed]]

--8<-- "pubsub/notifications/topic_unsubscribed.md:purpose"

--8<-- "pubsub/notifications/topic_unsubscribed.md:type"

### [[TopicAdvertReceived#topicadvertreceived]]

--8<-- "pubsub/notifications/topic_advert_received.md:purpose"

--8<-- "pubsub/notifications/topic_advert_received.md:type"

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

--8<-- "pubsub/messages/topic_advert.md:sequence"

--8<-- "pubsub/messages/event.md:sequence"

--8<-- "pubsub/messages/engine_message.md:sequence"

--8<-- "pubsub/messages/subscribe.md:sequence"

--8<-- "pubsub/messages/unsubscribe.md:sequence"

--8<-- "pubsub/messages/subscribe_request.md:sequence"

--8<-- "pubsub/messages/unsubscribe_request.md:sequence"

--8<-- "pubsub/messages/start_advert_request.md:sequence"

--8<-- "pubsub/messages/stop_advert_request.md:sequence"

--8<-- "pubsub/notifications/topic_subscribed.md:sequence"

--8<-- "pubsub/notifications/topic_unsubscribed.md:sequence"

--8<-- "pubsub/notifications/topic_advert_received.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>

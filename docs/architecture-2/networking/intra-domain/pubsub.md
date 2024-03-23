<div class="engine">

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

{{#include pubsub/types/pubsub-routing-table.md:purpose}}

## Messages received

### [[TopicAdvert#topicadvert]]

{{#include pubsub/messages/topic-advert.md:purpose}}

{{#include pubsub/messages/topic-advert.md:type}}

### [[Subscribe#subscribe]]

{{#include pubsub/messages/subscribe.md:purpose}}

{{#include pubsub/messages/subscribe.md:type}}

### [[Unsubscribe#unsubscribe]]

{{#include pubsub/messages/unsubscribe.md:purpose}}

{{#include pubsub/messages/unsubscribe.md:type}}

### [[Event#event]]

{{#include pubsub/messages/event.md:purpose}}

{{#include pubsub/messages/event.md:type}}

### [[EngineMessage to PubSub#enginemessage-pubsub|EngineMessage]]

{{#include pubsub/messages/engine-message.md:purpose}}

{{#include pubsub/messages/engine-message.md:type}}

### [[SubscribeRequest#subscriberequest]]

{{#include pubsub/messages/subscribe-request.md:purpose}}

{{#include pubsub/messages/subscribe-request.md:type}}

### [[UnsubscribeRequest#unsubscriberequest]]

{{#include pubsub/messages/unsubscribe-request.md:purpose}}

{{#include pubsub/messages/unsubscribe-request.md:type}}

### [[StartAdvertRequest#subscriberequest]]

{{#include pubsub/messages/start-advert-request.md:purpose}}

{{#include pubsub/messages/start-advert-request.md:type}}

### [[StopAdvertRequest#subscriberequest]]

{{#include pubsub/messages/stop-advert-request.md:purpose}}

{{#include pubsub/messages/stop-advert-request.md:type}}

## Notifications sent

### [[TopicSubscribed#topicsubscribed]]

{{#include pubsub/notifications/topic-subscribed.md:purpose}}

{{#include pubsub/notifications/topic-subscribed.md:type}}

### [[TopicUnsubscribed#topicunsubscribed]]

{{#include pubsub/notifications/topic-unsubscribed.md:purpose}}

{{#include pubsub/notifications/topic-unsubscribed.md:type}}

### [[TopicAdvertReceived#topicadvertreceived]]
 
{{#include pubsub/notifications/topic-advert-received.md:purpose}}

{{#include pubsub/notifications/topic-advert-received.md:type}}

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

{{#include pubsub/messages/topic-advert.md:sequence}}

{{#include pubsub/messages/event.md:sequence}}

{{#include pubsub/messages/engine-message.md:sequence}}

{{#include pubsub/messages/subscribe.md:sequence}}

{{#include pubsub/messages/unsubscribe.md:sequence}}

{{#include pubsub/messages/subscribe-request.md:sequence}}

{{#include pubsub/messages/unsubscribe-request.md:sequence}}

{{#include pubsub/messages/start-advert-request.md:sequence}}

{{#include pubsub/messages/stop-advert-request.md:sequence}}

{{#include pubsub/notifications/topic-subscribed.md:sequence}}

{{#include pubsub/notifications/topic-unsubscribed.md:sequence}}

{{#include pubsub/notifications/topic-advert-received.md:sequence}}
```
<!-- ANCHOR_END: messages -->

</div>

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

--8<-- "pubsub/types/pubsub-routing-table.md:purpose"

## Messages received

### [[TopicAdvert#topicadvert]]

--8<-- "pubsub/messages/topic-advert.md:purpose"

--8<-- "pubsub/messages/topic-advert.md:type"

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

--8<-- "pubsub/messages/engine-message.md:purpose"

--8<-- "pubsub/messages/engine-message.md:type"

### [[SubscribeRequest#subscriberequest]]

--8<-- "pubsub/messages/subscribe-request.md:purpose"

--8<-- "pubsub/messages/subscribe-request.md:type"

### [[UnsubscribeRequest#unsubscriberequest]]

--8<-- "pubsub/messages/unsubscribe-request.md:purpose"

--8<-- "pubsub/messages/unsubscribe-request.md:type"

### [[StartAdvertRequest#subscriberequest]]

--8<-- "pubsub/messages/start-advert-request.md:purpose"

--8<-- "pubsub/messages/start-advert-request.md:type"

### [[StopAdvertRequest#subscriberequest]]

--8<-- "pubsub/messages/stop-advert-request.md:purpose"

--8<-- "pubsub/messages/stop-advert-request.md:type"

## Notifications sent

### [[TopicSubscribed#topicsubscribed]]

--8<-- "pubsub/notifications/topic-subscribed.md:purpose"

--8<-- "pubsub/notifications/topic-subscribed.md:type"

### [[TopicUnsubscribed#topicunsubscribed]]

--8<-- "pubsub/notifications/topic-unsubscribed.md:purpose"

--8<-- "pubsub/notifications/topic-unsubscribed.md:type"

### [[TopicAdvertReceived#topicadvertreceived]]
 
--8<-- "pubsub/notifications/topic-advert-received.md:purpose"

--8<-- "pubsub/notifications/topic-advert-received.md:type"

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

--8<-- "pubsub/messages/topic-advert.md:sequence"

--8<-- "pubsub/messages/event.md:sequence"

--8<-- "pubsub/messages/engine-message.md:sequence"

--8<-- "pubsub/messages/subscribe.md:sequence"

--8<-- "pubsub/messages/unsubscribe.md:sequence"

--8<-- "pubsub/messages/subscribe-request.md:sequence"

--8<-- "pubsub/messages/unsubscribe-request.md:sequence"

--8<-- "pubsub/messages/start-advert-request.md:sequence"

--8<-- "pubsub/messages/stop-advert-request.md:sequence"

--8<-- "pubsub/notifications/topic-subscribed.md:sequence"

--8<-- "pubsub/notifications/topic-unsubscribed.md:sequence"

--8<-- "pubsub/notifications/topic-advert-received.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>

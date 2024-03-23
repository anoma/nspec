<div class="message">

# SubscribeRequest

## Purpose

<!-- ANCHOR: purpose -->
Subscription request.
<!-- ANCHOR_END: purpose -->

## Type

 <!-- ANCHOR: type -->
**Reception:**

[[TopicRequestV1#topicrequestv1]]

{{#include ../types/topic-request-v1.md:type}}

**Triggers:**

[[TopicResponseV1#topicresponsev1]]

{{#include ../types/topic-response-v1.md:type}}
<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
If not already subscribed, *PubSub* subscribes to the specified topic
by sending a P2P subscription request(s) to connected peers in the domain.
<!-- ANCHOR_END: behavior -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Router ->>+ PubSub: SubscribeRequest
PubSub -->>- Router: SubscribeResponse
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

</div>

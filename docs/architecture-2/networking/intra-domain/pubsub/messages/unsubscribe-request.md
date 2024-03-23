<div class="message">

# UnsubscribeRequest

## Purpose

<!-- ANCHOR: purpose -->
Unsubscription request.
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
If subscribed to the given topic, PubSub unsubscribes from it by sending P2P unsubscription requests to connected peers.
<!-- ANCHOR_END: behavior -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Router ->>+ PubSub: UnsubscribeRequest
PubSub -->>- Router: UnsubscribeResponse
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

</div>

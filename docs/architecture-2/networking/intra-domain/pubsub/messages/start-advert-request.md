<div class="message">

# StartAdvertRequest

## Purpose

<!-- ANCHOR: purpose -->
Start advertising a topic in the network.
<!-- ANCHOR_END: purpose -->

## Type

 <!-- ANCHOR: type -->
**Reception:**

[[TopicCreateRequestV1#topiccreaterequestv1]]

{{#include ../../../node/router/types/topic-create-request-v1.md:type}}

**Triggers:**

[[TopicResponseV1#topicresponsev1]]

{{#include ../types/topic-response-v1.md:type}}
<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Send [[TopicAdvert#topicadvert]] to connected neighbors in the domain.
<!-- ANCHOR_END: behavior -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Router ->>+ PubSub: StartAdvertRequest
PubSub -->>- Router: StartAdvertResponse
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

</div>

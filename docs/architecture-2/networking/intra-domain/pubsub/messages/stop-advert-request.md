<!-- ANCHOR_END: purpose -->
<div class="message">

# StopAdvertRequest

## Purpose

<!-- ANCHOR: purpose -->
Stop advertising a topic in the network.
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
<!-- ANCHOR_END: behavior -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Router ->>+ PubSub: StopAdvertRequest
PubSub -->>- Router: StopAdvertResponse
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

</div>

<div class="message">

# UnsubscribeAck

## Purpose

<!-- ANCHOR: purpose -->
Unsubscription acknowledgement.
<!-- ANCHOR_END: purpose -->

## Type

 <!-- ANCHOR: type -->
**Reception:**

[[TopicRequestV1#topicrequestv1]]

{{#include ../types/topic-request-v1.md:type}}

**Triggers:**

[[ToicUnsubscribed#topicunsubscribed]]

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
A [[TopicUnsubscribed#topicunsubscribed]] notification is sent to local engines.
<!-- ANCHOR_END: behavior -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
PubSub ->>+ PubSub_R: Unsubscribe
PubSub_R -->>- PubSub: UnsubscribeAck
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

</div>

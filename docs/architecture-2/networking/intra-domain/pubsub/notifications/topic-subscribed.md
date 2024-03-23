<div class="message">

# TopicSubscribed

## Purpose

 <!-- ANCHOR: purpose -->
Notification about a topic that was successfully subscribed at another peer.
 <!-- ANCHOR_END: purpose -->

## Type

 <!-- ANCHOR: type -->
[[TopicRequestV1#topicrequestv1]]

{{#include ../types/topic-request-v1.md:type}}
 <!-- ANCHOR_END: type -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
PubSub -) Any Local Engine: TopicSubscribed
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

</div>

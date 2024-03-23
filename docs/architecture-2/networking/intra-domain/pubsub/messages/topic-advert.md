# TopicAdvert

## Purpose

<!-- ANCHOR: purpose -->
Topic advertisement by a publisher.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[TopicAdvertV1#topicadvertv1]]

{{#include ../types/topic-advert-v1.md:type}}

**Triggers:**

*TopicAdvert*

[[TopicAdvertReceived#topicadvertreceived]]
<!-- ANCHOR_END: type -->


## Behavior

<!-- ANCHOR: behavior -->
Update topic routing table,
snd a [[TopicAdvertReceived#topicadvertreceived]] notification,
and forward the *TopicAdvert* to connected peers in the same domain.
<!-- ANCHOR_END: behavior -->

## Reception

<!-- ANCHOR: reception -->
- PubSub $\to$ *TopicAdvert* $\to$ PubSub
<!-- ANCHOR_END: reception -->


## Triggers

<!-- ANCHOR: triggers -->
- PubSub $\to$ *TopicAdvert* $\to$ PubSub
<!-- ANCHOR_END: triggers -->

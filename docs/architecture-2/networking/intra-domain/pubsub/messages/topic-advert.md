# TopicAdvert

## Purpose

<!-- --8<-- [start:purpose] -->
Topic advertisement by a publisher.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[TopicAdvertV1#topicadvertv1]]

{{#include ../types/topic-advert-v1.md:type}}

**Triggers:**

*TopicAdvert*

[[TopicAdvertReceived#topicadvertreceived]]
<!-- --8<-- [end:type] -->


## Behavior

<!-- --8<-- [start:behavior] -->
Update topic routing table,
snd a [[TopicAdvertReceived#topicadvertreceived]] notification,
and forward the *TopicAdvert* to connected peers in the same domain.
<!-- --8<-- [end:behavior] -->

## Reception

<!-- --8<-- [start:reception] -->
- PubSub $\to$ *TopicAdvert* $\to$ PubSub
<!-- --8<-- [end:reception] -->


## Triggers

<!-- --8<-- [start:triggers] -->
- PubSub $\to$ *TopicAdvert* $\to$ PubSub
<!-- --8<-- [end:triggers] -->

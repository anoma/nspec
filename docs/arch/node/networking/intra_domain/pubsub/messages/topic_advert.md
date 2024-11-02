---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TopicAdvert

## Purpose

<!-- --8<-- [start:purpose] -->
Topic advertisement by a publisher.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[TopicAdvertV1#topicadvertv1]]

--8<-- "../types/topic_advert_v1.md:type"

**Triggers:**

*TopicAdvert*

[[TopicAdvertReceived#topicadvertreceived]]
<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
Update topic routing table,
snd a [[TopicAdvertReceived#topicadvertreceived]] notification,
and forward the *TopicAdvert* to connected peers in the same domain.
<!-- --8<-- [end:behaviour] -->

## Reception

<!-- --8<-- [start:reception] -->
- PubSub $\to$ *TopicAdvert* $\to$ PubSub
<!-- --8<-- [end:reception] -->

## Triggers

<!-- --8<-- [start:triggers] -->
- PubSub $\to$ *TopicAdvert* $\to$ PubSub
<!-- --8<-- [end:triggers] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
%% --8<-- [start:sequence]
%% TODO
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

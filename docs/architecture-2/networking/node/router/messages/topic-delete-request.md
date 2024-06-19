---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# TopicDeleteRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Delete a pub/sub topic and remove all subscribers.

The request must come from the same engine that created the topic.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[TopicDeleteRequestV1#topicdeleterequestv1]]

--8<-- "../types/topic-delete-request-v1.md:type"

**Triggers:**

[[TopicDeleteResponseV1#topicdeleteresponsev1]]

--8<-- "../types/topic-delete-response-v1.md:type"
<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
The topic is removed from the [[RoutingTable#routingtable]] along with all subscribers.
<!-- --8<-- [end:behaviour] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Router: TopicDeleteRequest
Router ->>+ PubSub: StopAdvertRequest
PubSub -->>- Router: StopAdvertResponse
Router -->>- Any Local Engine: TopicDeleteResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

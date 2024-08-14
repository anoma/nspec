---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# UnsubscribeAck

## Purpose

<!-- --8<-- [start:purpose] -->
Unsubscription acknowledgement.
<!-- --8<-- [end:purpose] -->

## Type

 <!-- --8<-- [start:type] -->
**Reception:**

[[TopicRequestV1#topicrequestv1]]

--8<-- "../types/topic_request_v1.md:type"

**Triggers:**

[[ToicUnsubscribed#topicunsubscribed]]

<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
A [[TopicUnsubscribed#topicunsubscribed]] notification is sent to local engines.
<!-- --8<-- [end:behaviour] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
PubSub ->>+ PubSub_R: Unsubscribe
PubSub_R -->>- PubSub: UnsubscribeAck
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

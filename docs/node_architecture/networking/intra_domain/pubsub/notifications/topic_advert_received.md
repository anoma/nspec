---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# TopicAdvertReceived

## Purpose

<!-- --8<-- [start:purpose] -->
A [[TopicAdvert]] has been received from another peer.
<!-- --8<-- [end:purpose] -->

## Type

 <!-- --8<-- [start:type] -->
[[TopicCreateRequestV1#topiccreaterequestv1]]

--8<-- "../../../node/router/types/topic_create_request_v1.md:type"
 <!-- --8<-- [end:type] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
PubSub -) Any Local Engine: TopicAdvertReceived
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

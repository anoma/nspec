<div class="message" markdown>

# StopAdvertRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Stop advertising a topic in the network.
<!-- --8<-- [end:purpose] -->

## Type

 <!-- --8<-- [start:type] -->
**Reception:**

[[TopicRequestV1#topicrequestv1]]

--8<-- "../types/topic-request-v1.md:type"

**Triggers:**

[[TopicResponseV1#topicresponsev1]]

--8<-- "../types/topic-response-v1.md:type"
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Router ->>+ PubSub: StopAdvertRequest
PubSub -->>- Router: StopAdvertResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

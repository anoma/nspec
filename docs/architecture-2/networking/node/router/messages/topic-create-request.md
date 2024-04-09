<div class="message" markdown>


# TopicCreateRequest


## Purpose


<!-- --8<-- [start:purpose] -->
Create a pub/sub topic and start accepting subscriptions to it.
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
**Reception:**

[[TopicCreateRequestV1#topiccreaterequestv1]]

--8<-- "../types/topic-create-request-v1.md:type"

**Triggers:**

[[TopicCreateResponseV1#topiccreateresponsev1]]

--8<-- "../types/topic-create-response-v1.md:type"
<!-- --8<-- [end:type] -->

## Behavior


<!-- --8<-- [start:behavior] -->
The topic is added to the [[RoutingTable#routingtable]] with an initially empty subscriber list.
<!-- --8<-- [end:behavior] -->

## Message flow


<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Router: TopicCreateRequest
Router ->>+ PubSub: StartAdvertRequest
PubSub -->>- Router: StartAdvertResponse
Router -->>- Any Local Engine: TopicCreateResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

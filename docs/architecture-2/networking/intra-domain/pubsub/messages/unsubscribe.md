<div class="message" markdown>


# Unsubscribe

## Purpose

<!-- --8<-- [start:purpose] -->
Unsubscribe from a topic at other peers.
<!-- --8<-- [end:purpose] -->

## Type

 <!-- --8<-- [start:type] -->
**Reception:**

[[TopicRequestV1#topicrequestv1]]

--8<-- "../types/topic-request-v1.md:type"

**Triggers:**

[[UnsubscribeAck#SubscribeAck]]

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
The peer the request arrived from is removed from the [[PubSubRoutingTable#pubsubroutingtable]],
and an [[UnsubscribeAck#unsubscribeack]] is returned in response.
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
PubSub ->>+ PubSub_R: Unsubscribe
PubSub_R -->>- PubSub: UnsubscribeAck
%% ANCHOR_END: sequence
```
<!-- --8<-- [end:messages] -->

</div>

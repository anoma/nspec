<div class="message" markdown>


# SubscribeAck

## Purpose

<!-- --8<-- [start:purpose] -->
Subscription acknowledgement.
<!-- --8<-- [end:purpose] -->

## Type

 <!-- --8<-- [start:type] -->
**Reception:**

[[TopicRequestV1#topicrequestv1]]

--8<-- "../types/topic-request-v1.md:type"

**Triggers:**

[[TopicSubscribed#topicsubscribed]]

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
A [[TopicSubscribed#topicsubscribed]] notification is sent to local engines.
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
PubSub ->>+ PubSub_R: Subscribe
PubSub_R -->>- PubSub: SubscribeAck
%% ANCHOR_END: sequence
```
<!-- --8<-- [end:messages] -->

</div>

# TopicSubRequestV1

## Purpose

<!-- --8<-- [start:purpose] -->
Request to subscribe to a pub/sub topic.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type">

*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Pub/sub  topic identity*

- `scope`: [[RoutingScope#routingscope]]

  *Whether the subscription request is local-only or should be also sent to the network*

</div>
<!-- --8<-- [end:type] -->

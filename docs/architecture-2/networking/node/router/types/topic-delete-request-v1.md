# TopicDeleteRequestV1

## Purpose

<!-- --8<-- [start:purpose] -->
Request to delete a pub/sub topic.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Pub/sub topic identity.*

- `scope`: [[RoutingScope#routingscope]]

  *Whether the topic should be stopped being advertised on the network.*

</div>
<!-- --8<-- [end:type] -->

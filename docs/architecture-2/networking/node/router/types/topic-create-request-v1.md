# TopicCreateRequestV1

## Purpose

<!-- --8<-- [start:purpose] -->
Request to create a pub/sub topic.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Pub/sub topic identity.*

- `scope`: [[RoutingScope#routingscope]]

  *Whether the topic should be advertised over the network.*

- `advert`: Option\<[[TopicAdvertV1#topicadvertv1]]\>

  *Topic advertisement to send to the network, when the `scope` allows.*

</div>
<!-- --8<-- [end:type] -->

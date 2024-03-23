# TopicCreateRequestV1

## Purpose

<!-- ANCHOR: purpose -->
Request to create a pub/sub topic.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Pub/sub topic identity.*

- `scope`: [[RoutingScope#routingscope]]

  *Whether the topic should be advertised over the network.*

- `advert`: Option\<[[TopicAdvertV1#topicadvertv1]]\>

  *Topic advertisement to send to the network, when the `scope` allows.*

</div>
<!-- ANCHOR_END: type -->

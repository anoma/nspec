# TopicUnsubRequestV1

## Purpose

<!-- ANCHOR: purpose -->
Request to unsubscribe from a pub/sub topic.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Pub/sub  topic identity*

- `scope`: [[RoutingScope#routingscope]]

  *Whether the unsubscription request is local-only or should be also sent to the network*

</div>
<!-- ANCHOR_END: type -->

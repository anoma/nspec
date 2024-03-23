# TopicAdvertV1

## Purpose

<!-- ANCHOR: purpose -->
Topic advertisement.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Topic ID*

- `tags`: list\<string\>

  *List of optional tags to facilitate subscribing to new topics with relevant tags*

- `publisher`: [[EngineIdentity#engineidentity]]

  *PubSub engine ID of publisher*

- `created`: [[Time#time]]

  *Creation time*

- `sig`: [[Signature#signature]]

  *Signature over the above fields by `topic`*

</div>
<!-- ANCHOR_END: type -->

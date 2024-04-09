# TopicAdvertV1

## Purpose

<!-- --8<-- [start:purpose] -->
Topic advertisement.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

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
<!-- --8<-- [end:type] -->

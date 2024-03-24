# BlockSearchTopic

## Purpose

<!-- --8<-- [start:purpose] -->
Search for a block along the reverse publishing path of a pub/sub topic.
<!-- --8<-- [end:purpose] -->

## Reception

<!-- --8<-- [start:reception] -->
- Storage $\to$ *BlockSearchTopic* $\to$ Storage
<!-- --8<-- [end:reception] -->

## Structure

| Field   | Type                              | Description |
|---------|-----------------------------------|-------------|
| `block` | *[[BlockId#blockid]]*             | Block ID    |
| `topic` | *[[TopicIdentity#topicidentity]]* | Topic ID    |

## Behavior

If the block is available locally, a [[BlockSearchResponse#blocksearchresponse] is returned.
Otherwise the request is forwarded to the parent node in the pub/sub dissemination path for the given topic.

## Triggers

<!-- --8<-- [start:triggers] -->
- Storage $\to$ *BlockSearchTopic* $\to$ Storage
- Storage $\to$ *[[BlockResponse#blockresponse]]* $\to$ Storage
<!-- --8<-- [end:triggers] -->

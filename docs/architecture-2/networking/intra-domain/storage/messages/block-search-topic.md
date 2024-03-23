# BlockSearchTopic

## Purpose

<!-- ANCHOR: purpose -->
Search for a block along the reverse publishing path of a pub/sub topic.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Storage $\to$ *BlockSearchTopic* $\to$ Storage
<!-- ANCHOR_END: reception -->

## Structure

| Field   | Type                              | Description |
|---------|-----------------------------------|-------------|
| `block` | *[[BlockId#blockid]]*             | Block ID    |
| `topic` | *[[TopicIdentity#topicidentity]]* | Topic ID    |

## Behavior

If the block is available locally, a [[BlockSearchResponse#blocksearchresponse] is returned.
Otherwise the request is forwarded to the parent node in the pub/sub dissemination path for the given topic.

## Triggers

<!-- ANCHOR: triggers -->
- Storage $\to$ *BlockSearchTopic* $\to$ Storage
- Storage $\to$ *[[BlockResponse#blockresponse]]* $\to$ Storage
<!-- ANCHOR_END: triggers -->

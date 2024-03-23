# BlockLookupRequest

## Purpose

<!-- ANCHOR: purpose -->
Look up a block in local storage and on the network.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Any Local Engine $\to$ *BlockLookupRequest* $\to$ Storage
<!-- ANCHOR_END: reception -->

## Structure

| Field    | Type                                          | Description                          |
|----------|-----------------------------------------------|--------------------------------------|
| `block`  | *[[BlockId#blockid]]*                         | Block ID                             |
| `topic`  | *Option\<[[TopicIdentity#topicidentity]]\>*   | Enable search in a PubSub topic      |
| `random` | *bool*                                        | Enable search using random walk      |
| `domain` | *Option\<[[DomainIdentity#domainidentity]]\>* | Restrict the random walk to a domain |

## Behavior

First query the local storage for the block.
If not found, initiate a search on the network, when either `topic` or `random` is enabled.

## Triggers

<!-- ANCHOR: triggers -->
- Storage $\to$ *[[BlockResponse#blockresponse]]* $\to$ Any Local Engine
<!-- ANCHOR_END: triggers -->

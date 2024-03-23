# BlockSearchRandom

## Purpose

<!-- ANCHOR: purpose -->
Search for a block along a random walk.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Storage $\to$ *BlockSearchTopic* $\to$ Storage
<!-- ANCHOR_END: reception -->

## Structure

| Field       | Type                                          | Description                          |
|-------------|-----------------------------------------------|--------------------------------------|
| `block`     | *[[BlockId#blockid]]*                         | Block ID                             |
| `domain`    | *Option\<[[DomainIdentity#domainidentity]]\>* | Restrict the random walk to a domain |
| `requestor` | *[[NodeIdentity#nodeidentity]]*               | Requestor's Peer ID                  |

## Behavior

If the block is available locally, a [[BlockSearchResponse#blocksearchresponse] is returned to the requestor.
Otherwise the request is forwarded to a random connected node.
If a domain is given, the choice of random node is restricted to the given domain.

## Triggers

<!-- ANCHOR: triggers -->
- Storage $\to$ *BlockSearchRandom* $\to$ Storage
- Storage $\to$ *[[BlockResponse#blockresponse]]* $\to$ Storage
<!-- ANCHOR_END: triggers -->

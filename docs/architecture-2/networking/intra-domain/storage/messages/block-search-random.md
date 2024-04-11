---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# BlockSearchRandom

## Purpose

<!-- --8<-- [start:purpose] -->
Search for a block along a random walk.
<!-- --8<-- [end:purpose] -->

## Reception

<!-- --8<-- [start:reception] -->
- Storage $\to$ *BlockSearchTopic* $\to$ Storage
<!-- --8<-- [end:reception] -->

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

<!-- --8<-- [start:triggers] -->
- Storage $\to$ *BlockSearchRandom* $\to$ Storage
- Storage $\to$ *[[BlockResponse#blockresponse]]* $\to$ Storage
<!-- --8<-- [end:triggers] -->

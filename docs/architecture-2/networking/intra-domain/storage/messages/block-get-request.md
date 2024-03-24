# BlockGetRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Request contents of a block by its content hash ID.
<!-- --8<-- [end:purpose] -->

## Reception

<!-- --8<-- [start:reception] -->
- Any $\to$ *BlockGetRequest* $\to$ Storage
<!-- --8<-- [end:reception] -->

## Structure

| Field     | Type                  | Description   |
|-----------|-----------------------|---------------|
| `id`      | *[[BlockId#blockid]]* | Block ID      |

## Triggers

<!-- --8<-- [start:triggers] -->
- Storage $\to$ *[[BlockGetResponse#blockgetresponse]]* $\to$ Any
<!-- --8<-- [end:triggers] -->

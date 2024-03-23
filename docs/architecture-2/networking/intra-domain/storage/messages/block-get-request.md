# BlockGetRequest

## Purpose

<!-- ANCHOR: purpose -->
Request contents of a block by its content hash ID.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Any $\to$ *BlockGetRequest* $\to$ Storage
<!-- ANCHOR_END: reception -->

## Structure

| Field     | Type                  | Description   |
|-----------|-----------------------|---------------|
| `id`      | *[[BlockId#blockid]]* | Block ID      |

## Triggers

<!-- ANCHOR: triggers -->
- Storage $\to$ *[[BlockGetResponse#blockgetresponse]]* $\to$ Any
<!-- ANCHOR_END: triggers -->

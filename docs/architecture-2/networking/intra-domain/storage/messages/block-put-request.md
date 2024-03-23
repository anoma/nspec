# BlockPutRequest

## Purpose

<!-- ANCHOR: purpose -->
Request storing a block.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Any $\to$ *BlockPutRequest* $\to$ Storage
<!-- ANCHOR_END: reception -->

## Structure

| Field     | Type                  | Description               |
|-----------|-----------------------|---------------------------|
| `id`      | *[[BlockId#blockid]]* | Block ID                  |
| `content` | *Vec<u8>*             | Block content             |
| `prefs`   | *StoragePrefs*        | Block storage preferences |

## Triggers

<!-- ANCHOR: triggers -->
- Storage $\to$ *[[BlockPutResponse#blockputresponse]]* $\to$ Any
<!-- ANCHOR_END: triggers -->

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# BlockPutRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Request storing a block.
<!-- --8<-- [end:purpose] -->

## Reception

<!-- --8<-- [start:reception] -->
- Any $\to$ *BlockPutRequest* $\to$ Storage
<!-- --8<-- [end:reception] -->

## Structure

| Field     | Type                  | Description               |
|-----------|-----------------------|---------------------------|
| `id`      | *[[BlockId#blockid]]* | Block ID                  |
| `content` | *Vec<u8>*             | Block content             |
| `prefs`   | *StoragePrefs*        | Block storage preferences |

## Triggers

<!-- --8<-- [start:triggers] -->
- Storage $\to$ *[[BlockPutResponse#blockputresponse]]* $\to$ Any
<!-- --8<-- [end:triggers] -->

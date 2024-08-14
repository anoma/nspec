---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# StoragePrefs

## Purpose

<!-- --8<-- [start:purpose] -->
Storage preferences.
<!-- --8<-- [end:purpose] -->

## Type

*Struct* with the following fields.

| Field       | Type        | Description                                                           |
|-------------|-------------|-----------------------------------------------------------------------|
| `expiry`    | *Timestamp* | Expiry time after which the block is deleted.                         |
| `min_trust` | *u8*        | Minimum trust value required when serving the block to third parties. |

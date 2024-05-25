---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# SetValueKVStoreRequestV1

## Purpose

<!-- --8<-- [start:purpose] -->
Add a piece of data to the KV store by adding its key and the corresponding value.
If the key already exists, override the value.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:

- `Storage Key`: [[StorageKeyV1#storagekeyv1]]

  *The key that that identifies the piece of data in the KV-store.*

- `Storage Value`: [[StorageValueV1#storagevaluev1]]

  *The corresponding value that needs to be added to the KV-store.*

</div>
<!-- --8<-- [end:type] -->

## Values


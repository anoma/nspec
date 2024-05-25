---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ValueChangedKVStore

## Purpose

<!-- --8<-- [start:purpose] -->
When the value in the KV-store changes, engines interested in this information get notified.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:

- `Storage Key`: [[StorageKeyV1#storagekeyv1]]

  *The key that that identifies the changed piece of data in the KV-store.*

- `Storage Value`: [[StorageValueV1#storagevaluev1]]

  *The corresponding value that needs to be recorded in the KV-store.*

- `Epoch Timestamp`: [[EpochTimestamp#epochtimestamp]]

  *The wall clock time of the moment the value was changed.*

</div>
<!-- --8<-- [end:type] -->

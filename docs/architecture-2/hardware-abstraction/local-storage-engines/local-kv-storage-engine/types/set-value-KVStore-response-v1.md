# SetValueKVStoreResponseV1

## Purpose

<!-- --8<-- [start:purpose] -->
After adding the KV-pair to the KV-store, send a message indicating the success or failure of the operation.

<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Records* with fields:
- `Storage Key`: [[StorageKeyV1#storagekeyv1]]

  *The key that that identifies the piece of data in the KV-store.*

- `Success Operation`: [[SuccessOperationV1#successoperationv1]]

  *The success of the operation, indicating that the KV-pair was stored successfully or not.*

</div>
<!-- --8<-- [end:type] -->

## Values

<div class="message">

# DeleteValueKVStoreResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Response to [[DeleteValueKVStoreRequest#deletevaluekvstorerequest]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[DeleteValueKVStoreRequestV1#deletevaluekvstorerequestv1]]

{{#include ../types/delete-value-KVStore-response-v1.md:type}}

**Triggers**



<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
After deleting the KV-pair from the KV-store, send a message indicating the success or failure of the operation.
<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Dynamic Config Engine: GetDynamicConfigRequest
Dynamic Config Engine -->>- Any Local Engine: GetDynamicConfigResponse
%% ANCHOR_END: sequence
```

<!-- --8<-- [end:messages] -->

</div>
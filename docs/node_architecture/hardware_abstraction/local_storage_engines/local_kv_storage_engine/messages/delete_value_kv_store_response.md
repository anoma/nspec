---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# DeleteValueKVStoreResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Response to [[DeleteValueKVStoreRequest#deletevaluekvstorerequest]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[DeleteValueKVStoreRequestV1#deletevaluekvstorerequestv1]]

--8<-- "../types/delete_value_kv_store_response_v1.md:type"

**Triggers**

<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
After deleting the KV-pair from the KV-store, send a message indicating the success or failure of the operation.
<!-- --8<-- [end:behaviour] -->

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Dynamic Config Engine: GetDynamicConfigRequest
Dynamic Config Engine -->>- Any Local Engine: GetDynamicConfigResponse
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>

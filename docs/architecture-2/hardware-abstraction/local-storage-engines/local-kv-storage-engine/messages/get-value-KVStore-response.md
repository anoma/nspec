<div class="message">

# GetValueKVStoreResponse

## Purpose

<!-- ANCHOR: purpose -->
Return the value from the search operation which is triggered by a
[[GetValueKVStoreRequest#getvaluekvstorerequest]].

<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[GetValueKVStoreResponseV1#getvaluekvstoreresponsev1]]

{{#include ../types/get-value-KVStore-response-v1.md:type}}

**Triggers**


<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Returns the value from the search operation which is triggered by a 
[[GetValueKVStoreRequest#getvaluekvstorerequest]].

<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local KV Storage Engine: GetValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: GetValueKVStoreResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>
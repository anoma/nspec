<div class="message">

# GetValueKVStoreResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Return the value from the search operation which is triggered by a
[[GetValueKVStoreRequest#getvaluekvstorerequest]].

<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[GetValueKVStoreResponseV1#getvaluekvstoreresponsev1]]

--8<-- "../types/get-value-KVStore-response-v1.md:type"

**Triggers**


<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Returns the value from the search operation which is triggered by a 
[[GetValueKVStoreRequest#getvaluekvstorerequest]].

<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local KV Storage Engine: GetValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: GetValueKVStoreResponse
%% ANCHOR_END: sequence
```

<!-- --8<-- [end:messages] -->

</div>
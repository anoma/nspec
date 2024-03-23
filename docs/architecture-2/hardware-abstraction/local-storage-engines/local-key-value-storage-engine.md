<div class="engine">

# Local Key-Value Storage Engine

## Purpose

The *Local Key-Value Storage Engine* provides the local storage and retrieval of data in a key-value format. 

## State


## Messages received

### [[GetValueKVStoreRequest#getvaluekvstorerequest]]

{{#include local-kv-storage-engine/messages/get-value-KVStore-request.md:purpose}}

{{#include local-kv-storage-engine/messages/get-value-KVStore-request.md:type}}


### [[SetValueKVStoreRequest#setvaluekvstorerequest]]

{{#include local-kv-storage-engine/messages/set-value-KVStore-request.md:purpose}}

{{#include local-kv-storage-engine/messages/set-value-KVStore-request.md:type}}

### [[DeleteValueKVStoreRequest#deletevaluekvstorerequest]]

{{#include local-kv-storage-engine/messages/delete-value-KVStore-request.md:purpose}}

{{#include local-kv-storage-engine/messages/delete-value-KVStore-request.md:type}}

## Notifications sent

### [[ValueChangedKVStore#valuechangedkvstore]]

{{#include local-kv-storage-engine/notifications/value-changed-KVStore.md:purpose}}

{{#include local-kv-storage-engine/notifications/value-changed-KVStore.md:type}}

## Message Flow


 <!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local KV Storage Engine: GetValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: GetValueKVStoreResponse
Any Local Engine ->>+ Local KV Storage Engine: SetValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: SetValueKVStoreResponse
Any Local Engine ->>+ Local KV Storage Engine: DeleteValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: DeleteValueKVStoreResponse
%% ANCHOR_END: sequence
```
 <!-- ANCHOR_END: messages -->

</div>
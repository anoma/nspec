---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Local Key-Value Storage Engine

## Purpose

The *Local Key-Value Storage Engine* provides the local storage and retrieval of data in a key-value format. The storage is append-only, referencially transparent.

## State

## Messages received

### [[GetValueKVStoreRequest#getvaluekvstorerequest]]

--8<-- "local-kv-storage-engine/messages/get-value-KVStore-request.md:purpose"

--8<-- "local-kv-storage-engine/messages/get-value-KVStore-request.md:type"

### [[SetValueKVStoreRequest#setvaluekvstorerequest]]

--8<-- "local-kv-storage-engine/messages/set-value-KVStore-request.md:purpose"

--8<-- "local-kv-storage-engine/messages/set-value-KVStore-request.md:type"

### [[DeleteValueKVStoreRequest#deletevaluekvstorerequest]]

--8<-- "local-kv-storage-engine/messages/delete-value-KVStore-request.md:purpose"

--8<-- "local-kv-storage-engine/messages/delete-value-KVStore-request.md:type"

## Notifications sent

### [[ValueChangedKVStore#valuechangedkvstore]]

--8<-- "local-kv-storage-engine/notifications/value-changed-KVStore.md:purpose"

--8<-- "local-kv-storage-engine/notifications/value-changed-KVStore.md:type"

## Message Flow

 <!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Local KV Storage Engine: GetValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: GetValueKVStoreResponse
Any Local Engine ->>+ Local KV Storage Engine: SetValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: SetValueKVStoreResponse
Any Local Engine ->>+ Local KV Storage Engine: DeleteValueKVStoreRequest
Local KV Storage Engine -->>- Any Local Engine: DeleteValueKVStoreResponse
%% --8<-- [end:sequence]
```
 <!-- --8<-- [end:messages] -->

</div>

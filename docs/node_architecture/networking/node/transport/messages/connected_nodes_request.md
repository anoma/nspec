---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ConnectedNodesRequest

# ConnectedNodesResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Request the list of currently connected nodes.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

*unit*

**Triggers:**

[[ConnectedNodesResponseV1#connectednodesresponsev1]]

--8<-- "../types/connected_nodes_response_v1.md:type"
<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
Return the list of currently connected nodes from the [[ConnectionPool#connectionpool]].
<!-- --8<-- [end:behaviour] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Transport: ConnectedNodesRequest
Transport -->>- Any Local Engine: ConnectedNodesResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

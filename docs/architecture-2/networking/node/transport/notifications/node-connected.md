---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# NodeConnected

## Purpose

<!-- --8<-- [start:purpose] -->
Notification sent when a transport connection is established to a node.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
[[NodeTransportAddress#nodetransportaddress]]

--8<-- "../types/node-transport-address.md:type"
<!-- --8<-- [end:type] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Transport -) Any Local Engine: NodeConnected
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

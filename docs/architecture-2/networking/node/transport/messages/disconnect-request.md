---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# DisconnectRequest

# DisconnectResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Establish disconnection to a node.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[DisconnectRequestV1#disconnectrequestv1]]

--8<-- "../types/disconnect-request-v1.md:type"

**Triggers:**

[[DisconnectResponseV1#disconnectresponsev1]]

--8<-- "../types/disconnect-response-v1.md:type"
<!-- --8<-- [end:type] -->

## Behavior

Disconnect from the specified node, if connected.

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Topology ->>+ Transport: DisconnectRequest
Transport -->>- Topology: DisconnectResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

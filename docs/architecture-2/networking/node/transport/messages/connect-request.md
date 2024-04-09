<div class="message" markdown>

# ConnectRequest

# ConnectResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Establish connection to a node.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[ConnectRequestV1#connectrequestv1]]

--8<-- "../types/connect-request-v1.md:type"

**Triggers:**

[[ConnectResponseV1#connectresponsev1]]

--8<-- "../types/connect-response-v1.md:type"
<!-- --8<-- [end:type] -->

## Behavior

Establish connection to the specified node, if not yet connected.

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Topology ->>+ Transport: ConnectRequest
Transport -->>- Topology: ConnectResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

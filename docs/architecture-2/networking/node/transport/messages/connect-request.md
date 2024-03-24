<div class="message">

# ConnectRequest
# ConnectResponse

## Purpose

Establish connection to a node.

<!-- --8<-- [start:type] -->
**Reception:**

[[ConnectRequestV1#connectrequestv1]]

{{#include ../types/connect-request-v1.md:type}}

**Triggers:**

[[ConnectResponseV1#connectresponsev1]]

{{#include ../types/connect-response-v1.md:type}}
<!-- --8<-- [end:type] -->

## Behavior

Establish connection to the specified node, if not yet connected.

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Topology ->>+ Transport: ConnectRequest
Transport -->>- Topology: ConnectResponse
%% ANCHOR_END: sequence
```
<!-- --8<-- [end:messages] -->

</div>

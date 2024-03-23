# NodeConnectFailed

<!-- ANCHOR: purpose -->
Notification sent when failed to establish a connection to a node.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
[[NodeTransportAddress#nodetransportaddress]]

{{#include ../types/node-transport-address.md:type}}
<!-- ANCHOR_END: type -->

## Message flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Transport -) Any Local Engine: NodeConnectFailed
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

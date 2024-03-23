# NodeDisconnected

<!-- ANCHOR: purpose -->
Notification sent when a transport connection is closed to a node.
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
Transport -) Any Local Engine: NodeDisconnected
%% ANCHOR_END: sequence
```
<!-- ANCHOR_END: messages -->

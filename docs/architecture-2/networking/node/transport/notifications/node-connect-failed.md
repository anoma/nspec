# NodeConnectFailed

<!-- --8<-- [start:purpose] -->
Notification sent when failed to establish a connection to a node.
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
Transport -) Any Local Engine: NodeConnectFailed
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

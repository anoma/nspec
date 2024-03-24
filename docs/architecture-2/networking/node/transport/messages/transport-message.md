# TransportMessage

## Purpose

<!-- --8<-- [start:purpose] -->
A message from/to one of the transport protocols.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[TransportMessageV1#TransportMessagev1]]

{{#include ../types/transport-message-v1.md:type}}

**Triggers:**

[[P2PMessage#p2pmessage]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
When receiving a *TransportMessage* from one of the transport protocols
`addr` contains the source address,
`tprefs` and `expiry` are not set,
and `msg` contains the message received.
Upon reception, *Transport* forwards the contained *[[P2PMessage#p2pmessage]]* to the *[[Router#router]]*.

When sending a *TransportMessage* via one of the transport prototocols,
`addr` contains the destination address,
`tprefs` is set to the transport prefences from either the contained [[EngineMessage#enginemessage]],
the [[NodeIdentityRecord#nodeidentityrecord]] from the [[Network Identity Store#network-identity-store]],
or the defaults in the local configuration of the *Transport* engine,
`expiry` is set from the contained [[EngineMessage#enginemessage]],
and `msg` contains the message to be sent.
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
TransportProtocol -) Transport: TransportMessage
Transport -) Router: P2PMessage
Router -) Transport: P2PMessage
Transport -) TransportProtocol: TransportMessage
%% ANCHOR_END: sequence
```
<!-- --8<-- [end:messages] -->

</div>

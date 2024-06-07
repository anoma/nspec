---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# NodeMessage

## Purpose

<!-- --8<-- [start:purpose] -->
A signed message sent between two nodes.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[NodeMessageV1#nodemessagev1]]

--8<-- "../types/node-message-v1.md:type"

**Triggers:**

[[EngineMessage#enginemessage]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
The *Router* verifies the signature, and if valid, it processes the contained *[[EngineMessage#enginemessage]]* or *[[RelayMessage#relaymessage]]*.
Otherwise discards the message, and disconnects from the peer by sending a *[[DisconnectRequest#disconnectrequest]]* message to *[[Transport#transport]]*.
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Transport -) Router: NodeMessage
Router -) Any Local Engine: EngineMessage
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

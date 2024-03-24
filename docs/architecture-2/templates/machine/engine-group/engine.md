<div class="engine">

# Engine Name

## Purpose

<!-- --8<-- [start:purpose] -->
Describe the purpose of the engine.
<!-- --8<-- [end:purpose] -->

## State

<!-- List of types that are part of the state maintained by the engine. Optional -->

### [[TypeName#typename]]

{{#include engine/types/type-name.md:purpose}}

{{#include engine/types/type-name.md:type}}

## Messages received

<!-- List of messages received by the engine -->

### [[MessageName#messagename]]

{{#include engine/messages/message-name.md:purpose}}

{{#include engine/messages/message-name.md:type}}

## Notifications sent

<!-- List of notifications sent by the engine. Optional -->

### [[NotificationName#notificationname]]

{{#include engine/notifications/notification-name.md:purpose}}

{{#include engine/notifications/notification-name.md:typee}}

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

{{#include engine/messages/message-name.md:sequence}}

{{#include engine/messages/other-message-name.md:sequence}}
```
<!-- --8<-- [end:messages] -->

</div>

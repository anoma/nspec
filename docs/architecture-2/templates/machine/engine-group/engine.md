<div class="engine" markdown>


# Engine Name

## Purpose

<!-- --8<-- [start:purpose] -->
Describe the purpose of the engine.
<!-- --8<-- [end:purpose] -->

## State

<!-- List of types that are part of the state maintained by the engine. Optional -->

### [[TypeName#typename]]

<!-- --8<-- "engine/types/type-name.md:purpose" FIXME -->

<!-- --8<-- "engine/types/type-name.md:type" FIXME -->

## Messages received

<!-- List of messages received by the engine -->

### [[MessageName#messagename]]

<!-- --8<-- "engine/messages/message-name.md:purpose" FIXME -->

<!-- --8<-- "engine/messages/message-name.md:type" FIXME -->

## Notifications sent

<!-- List of notifications sent by the engine. Optional -->

### [[NotificationName#notificationname]]

<!-- --8<-- "engine/notifications/notification-name.md:purpose" FIXME -->

<!-- --8<-- "engine/notifications/notification-name.md:typee" FIXME -->

## Message flow

<!-- Sequence diagram for the engine with all messages -->

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- "engine/messages/message-name.md:sequence" FIXME

%% --8<-- "engine/messages/other-message-name.md:sequence" FIXME
```
<!-- --8<-- [end:messages] -->

</div>

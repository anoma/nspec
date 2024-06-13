---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Local Wall Clock Engine

## Purpose

<!-- --8<-- [start:purpose] -->

The *Local Wall Clock Engine* provides a mechanism for tracking and managing time locally on the physical machine that the Anoma node is running.
It abstracts away the details of the underlying hardware and
provides an interface for getting real-time clock functionality.

<!-- --8<-- [end:purpose] -->

## State

## Messages Received

### [[LocalWallClockGetTime#localwallclockgettime]]

--8<-- "local-wall-clock-engine/messages/local-wall-clock-get-time.md:purpose"

--8<-- "local-wall-clock-engine/messages/local-wall-clock-get-time.md:type"

## Notifications Sent

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram
--8<-- "local-wall-clock-engine/messages/local-wall-clock-get-time.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>

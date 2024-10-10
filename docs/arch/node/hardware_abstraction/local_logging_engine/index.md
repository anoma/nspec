---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Local Logging Engine

## Purpose

<!-- --8<-- [start:purpose] -->

The *Local Logging Engine* provides capabilities for recording, monitoring,
analyzing, and managing events and activities locally on the physical machine
that the Anoma node is running. It supports diagnostic efforts, security
monitoring, performance optimization, and historical analysis to ensure the
stability, security, and efficiency.

<!-- --8<-- [end:purpose] -->

## State

## Messages Received

### [[LocalLoggingAppend#localloggingappend]]

--8<-- "local_logging_engine/messages/local_logging_append.md:purpose"

--8<-- "local_logging_engine/messages/local_logging_append.md:type"

## Notifications Sent

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram
--8<-- "local_logging_engine/messages/local_logging_append.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>

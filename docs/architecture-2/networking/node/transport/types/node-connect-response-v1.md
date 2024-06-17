---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# NodeConnectResponseV1

## Purpose

<!-- --8<-- [start:purpose] -->
Response to a [[ConnectRequestV1]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Result*

</div>
<!-- --8<-- [end:type] -->

## Values

- *OK_CONNECTED*: connection is already established.
- *OK_LOOKUP*: connection establishment initiated after successful address lookup.
- *ERROR_LOOKUP*: node address lookup failed.

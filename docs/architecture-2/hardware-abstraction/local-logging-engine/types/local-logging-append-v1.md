---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# LocalLoggingAppendV1

## Purpose

<!-- --8<-- [start:purpose] -->
Append new values to the logbook.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:
- `external identity`: [[ExternalIdentity#externalidentity]]

  *External identity of the engine that wants to append the values to the logbook*

- `append value`: [[AppendValueV1#appendvaluev1]]

  *The value in a string format, which needs to be added to the logbook*

</div>
<!-- --8<-- [end:type] -->

## Values


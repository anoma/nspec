---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# P2PMessageV1

## Purpose

<!-- --8<-- [start:purpose] -->
Message between two nodes.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `src`: [[NodeIdentity#nodeidentity]]

  *Source peer*

- `dst`: [[NodeIdentity#nodeidentity]]

  *Destination peer*

- `msg`: enum { [[EngineMessageV1#enginemessagev1]], [[RelayMessageV1#relaymessagev1]] }

  *Encapsulated message*

- `sig`: [[Signature#signature]]

  *Signature over the above fields by `src`*

</div>
<!-- --8<-- [end:type] -->

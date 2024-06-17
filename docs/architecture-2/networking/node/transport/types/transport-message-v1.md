---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TransportMessageV1

## Purpose

<!-- --8<-- [start:purpose] -->
Describe the purpose of the type.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `addr`: [[TransportAddress]]

  *Source or destination address*

- `tprefs`: Option<[[TransportPrefs]]>

  *Transport preferences for outgoing messages*

- `expiry`: Option<[[Time]]>

  *Expiry time for outgoing messages*

- `msg`: [[EngineMessageV1]]

  *Encapsulated message*

</div>
<!-- --8<-- [end:type] -->

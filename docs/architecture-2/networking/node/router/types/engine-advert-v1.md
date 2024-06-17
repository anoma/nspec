---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# EngineAdvert

# EngineAdvertV1

## Purpose

<!-- --8<-- [start:purpose] -->
Advertisement of an engine instance that specifies its name, the node where it is running, and an optional hash key.
This allows to derive the [[EngineIdentity]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `name`: Vec<u8>

  *Engine name*

- `node`: [[NodeIdentity#nodeidentity]]

  *Node ID where the engine is running*

- `key`: Option<Vec<u8>>

  *Key for hash*

- `version`: u32

  *Version number*

- `created`: [[Time#time]]

  *Time of creation*

- `sig`: [[Signature#Signature]]

  *Signature by `id`*

</div>
<!-- --8<-- [end:type] -->

## See also

- [[EngineIdentity]]

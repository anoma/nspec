# EngineAdvert

# EngineAdvertV1

## Purpose

<!-- --8<-- [start:purpose] -->
Advertisement of an engine that specifies the node where it is running.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Record* with fields:

- `id`: [[EngineIdentity#engineidentity]]

  *Node ID*

- `node`: [[NodeIdentity#nodeidentity]]

  *Node ID where the engine is running*

- `version`: u32

  *Version number*

- `created`: [[Time#time]]

  *Time of creation*

- `sig`: [[Signature#Signature]]

  *Signature by `id`*

</div>
<!-- --8<-- [end:type] -->

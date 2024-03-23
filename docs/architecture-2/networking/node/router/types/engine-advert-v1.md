# EngineAdvert

# EngineAdvertV1

## Purpose

<!-- ANCHOR: purpose -->
Advertisement of an engine that specifies the node where it is running.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

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
<!-- ANCHOR_END: type -->

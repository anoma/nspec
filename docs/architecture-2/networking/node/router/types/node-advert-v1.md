---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# NodeAdvert

# NodeAdvertV1

## Purpose

<!-- --8<-- [start:purpose] -->
Advertisement of a peer's transport addresses.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `id`: [[NodeIdentity#nodeidentity]]

  *Node ID*

- `addrs`: Vec\<([[TransportAddress]], u8)\>

  *Transport addresses with preferences expressed as weights*

- `version`: u32

  *Version number*

- `created`: [[Time#time]]

  *Time of creation*

- `sig`: [[Signature#Signature]]

  *Signature by `id`*

</div>
<!-- --8<-- [end:type] -->

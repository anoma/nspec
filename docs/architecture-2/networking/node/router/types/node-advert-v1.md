# NodeAdvert

# NodeAdvertV1

## Purpose

<!-- ANCHOR: purpose -->
Advertisement of a peer's transport addresses.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

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
<!-- ANCHOR_END: type -->

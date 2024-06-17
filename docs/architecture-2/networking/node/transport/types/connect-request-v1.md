---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---
 
# ConnectRequestV1

## Purpose

<!-- --8<-- [start:purpose] -->
Request a connection to a node.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `nonce`: Vec<u8>

  *Nonce for challenge*

- `src`: [[NodeIdentity]]

  *Source node*

- `dst`: [[Digest]]

  *Destination node:*

  $keyed\_hash(key: nonce, input: NodeIdentity)$

- `src_advert_version`: Option<u32>

- `dst_advert_version`: u32


</div>
<!-- --8<-- [end:type] -->

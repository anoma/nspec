# P2PMessageV1

## Purpose

<!-- ANCHOR: purpose -->
Message between two nodes.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

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
<!-- ANCHOR_END: type -->

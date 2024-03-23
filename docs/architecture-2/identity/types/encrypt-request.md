# EncryptRequest

## Purpose

<!-- ANCHOR: purpose -->
An `EncryptRequest` instructs an encryption engine to encrypt data to a particular external identity, possibly using known reads-for relationships.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
*Record* with fields:

- `data`: `[]byte`

  *Data which to encrypt*

- `externalIdentity`: [[ExternalIdentity]]

  *External identity to encrypt to*

- `useReadsFor`: boolean

  *Whether or not to use known reads-for relationships*
</div>
<!-- ANCHOR_END: type -->
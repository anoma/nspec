# VerifyRequest

## Purpose

<!-- ANCHOR: purpose -->
A `VerifyRequest` instructs a verification engine to verify a commitment from a particular external identity, possibly using known signs-for relationships.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
*Record* with fields:

- `commitment`: [[Commitment]]

  *Commitment to verify*

- `data`: `[]byte`

  *Data to check the commitment against*

- `externalIdentity`: [[ExternalIdentity]]

  *External identity to verify this commitment from*

- `useSignsFor`: boolean

  *Whether or not to use known signs-for relationships
</div>
<!-- ANCHOR_END: type -->
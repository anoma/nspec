---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# VerifyRequest

## Purpose

<!-- --8<-- [start:purpose] -->
A `VerifyRequest` instructs a verification engine to verify a commitment from a particular external identity, possibly using known signs-for relationships.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

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
<!-- --8<-- [end:type] -->

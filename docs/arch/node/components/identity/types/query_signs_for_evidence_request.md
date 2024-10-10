---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# QuerySignsForEvidenceRequest

## Purpose

<!-- --8<-- [start:purpose] -->
A `QuerySignsForEvidenceRequest` instructs the signs_for engine to read and return the known signs_for evidence associated with a specific external identity.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `externalIdentity`: [[ExternalIdentity]]

  *The external identity to query*
</div>
<!-- --8<-- [end:type] -->

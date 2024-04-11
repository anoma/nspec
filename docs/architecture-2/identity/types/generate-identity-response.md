---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# GenerateIdentityResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `GenerateIdentityResponse` provides the handles to decryption and commitment engine instances for a newly generated identity, or an error if a failure occurred.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `commitmentEngine`: Maybe<[[EngineId]]>

  *Reference to newly instantiated commitment engine*

- `decryptionEngine`: Maybe<[[EngineId]]>

  *Reference to newly instantiated decryption engine*

- `externalIdentity`: [[ExternalIdentity]]

  *External identity of newly created identity*

- `error`: Maybe<string>

  *Error in identity generation, if applicable*
</div>
<!-- --8<-- [end:type] -->

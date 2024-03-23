# GenerateIdentityResponse

## Purpose

<!-- ANCHOR: purpose -->
A `GenerateIdentityResponse` provides the handles to decryption and commitment engine instances for a newly generated identity, or an error if a failure occurred.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
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
<!-- ANCHOR_END: type -->
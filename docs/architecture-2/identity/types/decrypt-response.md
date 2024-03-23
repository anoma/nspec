# DecryptResponse

## Purpose

<!-- ANCHOR: purpose -->
A `DecryptResponse` contains the data decrypted by a decryption engine instance in response to a [[DecryptRequest]].
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
*Record* with fields:

- `data`: `[]byte`

  *Decrypted data*

- `error`: `Maybe<string>`

  *Error in decryption, if applicable*
</div>
<!-- ANCHOR_END: type -->
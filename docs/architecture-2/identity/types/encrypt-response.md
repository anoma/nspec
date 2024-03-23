# EncryptResponse

## Purpose

<!-- ANCHOR: purpose -->
An `EncryptResponse` contains the data encrypted by an encryption engine in response to an [[EncryptRequest]].
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
*Record* with fields:

- `ciphertext`: `[]byte`

  *Encrypted ciphertext*

- `error`: `Maybe<string>`

  *Error in encryption, if applicable*
</div>
<!-- ANCHOR_END: type -->
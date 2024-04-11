---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# EncryptResponse

## Purpose

<!-- --8<-- [start:purpose] -->
An `EncryptResponse` contains the data encrypted by an encryption engine in response to an [[EncryptRequest]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `ciphertext`: `[]byte`

  *Encrypted ciphertext*

- `error`: `Maybe<string>`

  *Error in encryption, if applicable*
</div>
<!-- --8<-- [end:type] -->

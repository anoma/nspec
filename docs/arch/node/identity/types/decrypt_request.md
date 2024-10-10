---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# DecryptRequest

## Purpose

<!-- --8<-- [start:purpose] -->
A `DecryptRequest` instructs a decryption engine instance to decrypt data as the internal identity corresponding to that engine instance.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `data`: `[]byte`

  *Encrypted ciphertext to decrypt**
</div>
<!-- --8<-- [end:type] -->

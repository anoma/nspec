# DecryptResponse


## Purpose


<!-- --8<-- [start:purpose] -->
A `DecryptResponse` contains the data decrypted by a decryption engine instance in response to a [[DecryptRequest]].
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `data`: `[]byte`

  *Decrypted data*

- `error`: `Maybe<string>`

  *Error in decryption, if applicable*
</div>
<!-- --8<-- [end:type] -->

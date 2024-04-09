# GenerateIdentityRequest


## Purpose


<!-- --8<-- [start:purpose] -->
A `GenerateIdentityRequest` instructs the identity management engine to generate a new identity using the specified backend.
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `backend`: [[Backend]]

  *The backend to use*

- `params`: [[Params]]

  *Parameters to pass to the backend (e.g. cryptosystem, security level)*

- `capabilities`: [[Capabilities]]

  *Capabilities to request (decryption, commitment, or both)
</div>
<!-- --8<-- [end:type] -->

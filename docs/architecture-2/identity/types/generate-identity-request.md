# GenerateIdentityRequest

## Purpose

<!-- ANCHOR: purpose -->
A `GenerateIdentityRequest` instructs the identity management engine to generate a new identity using the specified backend.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
*Record* with fields:

- `backend`: [[Backend]]

  *The backend to use*

- `params`: [[Params]]

  *Parameters to pass to the backend (e.g. cryptosystem, security level)*

- `capabilities`: [[Capabilities]]

  *Capabilities to request (decryption, commitment, or both)
</div>
<!-- ANCHOR_END: type -->
# ConnectIdentityRequest

## Purpose

<!-- ANCHOR: purpose -->
A `ConnectIdentityRequest` instructs the identity management engine to connect an existing identity using the specified backend.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
*Record* with fields:

- `externalIdentity`: *[[ExternalIdentity]]*

  *The external identity to connect*
- `backend`: *[[Backend]]*
  
  *The backend to use*

- `capabilities`: *[[Capabilities]]*

  *The capabilities to request*
</div>
<!-- ANCHOR_END: type -->
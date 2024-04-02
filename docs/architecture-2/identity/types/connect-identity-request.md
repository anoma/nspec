# ConnectIdentityRequest

## Purpose

<!-- --8<-- [start:purpose] -->
A `ConnectIdentityRequest` instructs the identity management engine to connect an existing identity using the specified backend.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `externalIdentity`: *[[ExternalIdentity]]*

  *The external identity to connect*
- `backend`: *[[Backend]]*

  *The backend to use*

- `capabilities`: *[[Capabilities]]*

  *The capabilities to request*
</div>
<!-- --8<-- [end:type] -->

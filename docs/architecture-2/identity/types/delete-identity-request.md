# DeleteIdentityRequest

## Purpose

<!-- ANCHOR: purpose -->
A `DeleteIdentityRequest` instructs the identity management engine to delete an existing identity using the specified backend.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
| Field        | Type                    | Description |
|--------------|-------------------------|-------------|
| `externalIdentity` | ExternalIdentity | The external identity to delete |
| `backend` | *[Backend](../types/backend.md)* | The backend to use  |


*Record* with fields:

- `externalIdentity`: [[ExternalIdentity]]

  *The external identity to delete*

- `backend`: [[Backend]]

  *The backend to use*

</div>
<!-- ANCHOR_END: type -->
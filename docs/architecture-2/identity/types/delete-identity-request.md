# DeleteIdentityRequest

## Purpose

<!-- --8<-- [start:purpose] -->
A `DeleteIdentityRequest` instructs the identity management engine to delete an existing identity using the specified backend.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

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
<!-- --8<-- [end:type] -->
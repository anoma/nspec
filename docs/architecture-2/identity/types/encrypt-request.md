# EncryptRequest


## Purpose


<!-- --8<-- [start:purpose] -->
An `EncryptRequest` instructs an encryption engine to encrypt data to a particular external identity, possibly using known reads-for relationships.
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `data`: `[]byte`

  *Data which to encrypt*

- `externalIdentity`: [[ExternalIdentity]]

  *External identity to encrypt to*

- `useReadsFor`: boolean

  *Whether or not to use known reads-for relationships*
</div>
<!-- --8<-- [end:type] -->

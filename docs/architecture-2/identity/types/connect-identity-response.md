---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ConnectIdentityResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `ConnectIdentityResponse` provides the handles to decryption and commitment engine instances for a newly connected identity, or an error if a failure occurred.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

| Field        | Type                    | Description |
|--------------|-------------------------|-------------|
| `commitmentEngine` | Maybe<[[Commitment]] engine reference> | Reference to newly instantiated commitment engine |
| `decryptionEngine` | Maybe<[[Decryption]] engine reference> | Reference to newly instantiated decryption engine |
| `error` | string (tbd) | Error in identity connectionn, if applicable |

*Record* with fields:

- `commitmentEngine`: Maybe<[[EngineId]]>

  *Reference to newly instantiated commitment engine*
- `decryptionEngine`: Maybe<[[EngineId]]>

  *Reference to newly instantiated commitment engine*
- `error`: *Maybe<string>*

  *Error in identity connection, if applicable*
</div>
<!-- --8<-- [end:type] -->

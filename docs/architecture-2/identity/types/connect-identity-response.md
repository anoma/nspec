# ConnectIdentityResponse

## Purpose

<!-- ANCHOR: purpose -->
A `ConnectIdentityResponse` provides the handles to decryption and commitment engine instances for a newly connected identity, or an error if a failure occurred.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
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
<!-- ANCHOR_END: type -->
---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-behaviour
tags:
- decryption
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.decryption_messages;
    import prelude open;
    import arch.node.types.identities open;
    ```

# `Decryption` Messages

## Message interface

<!-- --8<-- [start:DecryptionMsg] -->
```juvix
type DecryptionMsg :=
  | -- --8<-- [start:DecryptRequest]
    DecryptRequest {
      data : Ciphertext
    }
    -- --8<-- [end:DecryptRequest]
  | -- --8<-- [start:DecryptResponse]
    DecryptResponse {
      data : Plaintext;
      err : Option String
    }
    -- --8<-- [end:DecryptResponse]
  ;
```
<!-- --8<-- [end:DecryptionMsg] -->

### `DecryptRequest` message

!!! quote "DecryptRequest"

    ```
    --8<-- "./decryption_messages.juvix.md:DecryptRequest"
    ```

A `DecryptRequest` instructs a decryption engine instance to decrypt data as the
internal identity corresponding to that engine instance.

- `data`: The encrypted ciphertext to decrypt.

### `DecryptResponse` message

!!! quote "DecryptResponse"

    ```
    --8<-- "./decryption_messages.juvix.md:DecryptResponse"
    ```

A `DecryptResponse` contains the data decrypted by a decryption engine instance
in response to a `DecryptRequest`.

- `data`: The decrypted data.
- `err`: An error message if decryption failed.

## Message sequence diagrams

### Decryption Sequence

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant C as Client
    participant DE as Decryption Engine

    C->>DE: DecryptRequest(encryptedData)
    Note over DE: Attempt to decrypt data
    alt Decryption Successful
        DE-->>C: DecryptResponse(decryptedData, err=none)
    else Decryption Failed
        DE-->>C: DecryptResponse(emptyByteString, err="Decryption Failed")
    end
```

<figcaption markdown="span">
Sequence diagram for decryption.
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->

## Engine Components

- [[Decryption Environment|`Decryption` Engine Environment]]
- [[Decryption Dynamics|`Decryption` Engine Dynamics]]

## Useful links


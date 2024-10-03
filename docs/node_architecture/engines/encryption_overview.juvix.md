---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- encryption
- engine-overview
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.encryption_overview;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.types.identity_types open;
    ```

# `Encryption` Engine Family Overview

--8<-- "./docs/node_architecture/engines/encryption.juvix.md:encryption-engine-family"

The Encryption engine is responsible for encrypting data to external identities, possibly using known `reads_for` relationships. It automatically utilizes "reads_for" relationship information from the Reads For Engine along with caller preference information to choose which identity to encrypt to.

## Purpose

The Encryption Engine encrypts data to external identities, optionally using known `reads_for` relationships. It is a stateless function, and calls to it do not need to be ordered. The runtime should implement this intelligently for efficiency.

## Message interface

<!-- --8<-- [start:EncryptionMsg] -->
```juvix
type EncryptionMsg :=
  | -- --8<-- [start:EncryptRequest]
    EncryptRequest {
      data : ByteString;
      externalIdentity : ExternalIdentity;
      useReadsFor : Bool
    }
    -- --8<-- [end:EncryptRequest]
  | -- --8<-- [start:EncryptResponse]
    EncryptResponse {
      ciphertext : ByteString;
      error : Maybe String
    }
    -- --8<-- [end:EncryptResponse]
  ;
```
<!-- --8<-- [end:EncryptionMsg] -->

### `EncryptRequest` message

!!! quote "EncryptRequest"

    ```
    --8<-- "./encryption_overview.juvix.md:EncryptRequest"
    ```

An `EncryptRequest` instructs the Encryption Engine to encrypt data to a particular external identity, possibly using known reads_for relationships.

- `data`: The data to encrypt.
- `externalIdentity`: The external identity to encrypt to.
- `useReadsFor`: Whether or not to use known `reads_for` relationships.

### `EncryptResponse` message

!!! quote "EncryptResponse"

    ```
    --8<-- "./encryption_overview.juvix.md:EncryptResponse"
    ```

An `EncryptResponse` contains the data encrypted by the Encryption Engine in response to an EncryptRequest.

- `ciphertext`: The encrypted data.
- `error`: An error message if encryption failed.

## Message sequence diagrams

### Encryption Sequence

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant EncryptionEngine
    participant ReadsForEngine

    Client ->> EncryptionEngine: EncryptRequest
    alt useReadsFor is true
        EncryptionEngine ->> ReadsForEngine: ReadsForRequest
        ReadsForEngine -->> EncryptionEngine: ReadsForResponse
    end
    EncryptionEngine ->> EncryptionEngine: Encrypt Data
    EncryptionEngine -->> Client: EncryptResponse
```

<figcaption markdown="span">
Sequence diagram for encryption, including optional ReadsFor interaction.
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->

## Engine Components

- [[encryption_environment|`Encryption` Engine Environment]]
- [[encryption_dynamics|`Encryption` Engine Dynamics]]

## Useful links

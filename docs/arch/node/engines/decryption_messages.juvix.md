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

# Decryption Messages

## Message interface

--8<-- "./decryption_messages.juvix.md:DecryptionMsg"

## Message sequence diagrams

---

### Request sequence

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant C as Client
    participant DE as Decryption Engine

    C->>DE: RequestDecryption(encryptedData)
    Note over DE: Attempt to decrypt data
    alt Decryption Successful
        DE-->>C: ResponseDecryption(decryptedData, err=none)
    else Decryption Failed
        DE-->>C: ResponseDecryption(emptyByteString, err="Decryption Failed")
    end
```

<figcaption markdown="span">
Sequence diagram for decryption.
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->

---

## Message types

---

### `RequestDecryption`

```juvix
type RequestDecryption := mkRequestDecryption {
  data : Ciphertext
};
```

A `RequestDecryption` instructs a decryption engine instance to decrypt data.

???+ quote "Arguments"
    `data`:
    : The encrypted ciphertext to decrypt.

---

### `ResponseDecryption`

```juvix
type ResponseDecryption := mkResponseDecryption {
  data : Plaintext;
  err : Option String
};
```

A `ResponseDecryption` contains the data decrypted by a decryption engine instance
in response to a `RequestDecryption`.

???+ quote "Arguments"

    `data`:
    : The decrypted data.

    `err`:
    : An error message if decryption failed.

---

### `DecryptionMsg`

<!-- --8<-- [start:DecryptionMsg] -->
```juvix
type DecryptionMsg :=
  | MsgDecryptionRequest RequestDecryption
  | MsgDecryptionResponse ResponseDecryption
  ;
```
<!-- --8<-- [end:DecryptionMsg] -->

---

## Engine Components

- [[Decryption Configuration]]
- [[Decryption Environment]]
- [[Decryption Behaviour]]
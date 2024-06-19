---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Identity Machine

The identity machine is responsible for management of data and operations related to identities, including:

- creating & deleting identities, handled by the [Identity Management Engine](./identity-management/index.md)

- encrypting to & decrypting as identities, handled by the [Encryption Engine](./encryption/index.md) and [Decryption Engine](./decryption/index.md)

    - In general, a node has only one [Encryption Engine](./encryption/index.md) and one [Decryption Engine](./decryption/index.md). Each [[EncryptRequest]] or [[VerifyRequest]] specifies what identity they're referring to.

- creating & verifying commitments, handled by the [Commitment Engine](./commitment/index.md) and [Verification Engine](./verification/index.md)

  - Note that there is a [Commitment Engine](./commitment/index.md) and/or a [Verification Engine](./verification/index.md) created on a node for each identity the node has. References to the [Commitment Engine](./commitment/index.md) and/or [Verification Engine](./verification/index.md) can be used as a kind of permission, ensuring that only processes which have been given such a reference will be able to commit or verify with a specific identity.

- tracking relationships between identities, including

    - which identities can sign for other identities, handled by the [Signs For Engine](./signs-for/index.md)

    - which identities can read for other identities, handled by the [Reads For Engine](./reads-for/index.md)

- tracking names associated to identities, handled by the [Name Engine](./name/index.md)

An _identity_ is as defined in [Identity](./../../architecture-1/abstractions/identity.md).

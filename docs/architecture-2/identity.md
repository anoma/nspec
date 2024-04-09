# Identity Machine


The identity machine is responsible for management of data and operations related to identities, including:
- creating & deleting identities, handled by the [Identity Management Engine](./identity/identity-management.md)
- encrypting to & decrypting as identities, handled by the [Encryption Engine](./identity/encryption.md) and [Decryption Engine](./identity/decryption.md)
  - In general, a node has only one [Encryption Engine](./identity/encryption.md) and one [Decryption Engine](./identity/decryption.md). Each [[EncryptRequest]] or [[VerifyRequest]] specifies what identity they're referring to.
- creating & verifying commitments, handled by the [Commitment Engine](./identity/commitment.md) and [Verification Engine](./identity/verification.md)
  - Note that there is a [Commitment Engine](./identity/commitment.md) and/or a [Verification Engine](./identity/verification.md) created on a node for each identity the node has. References to the [Commitment Engine](./identity/commitment.md) and/or [Verification Engine](./identity/verification.md) can be used as a kind of permission, ensuring that only processes which have been given such a reference will be able to commit or verify with a specific identity.
- tracking relationships between identities, including
    - which identities can sign for other identities, handled by the [Signs For Engine](./identity/signs-for.md)
    - which identities can read for other identities, handled by the [Reads For Engine](./identity/reads-for.md)
- tracking names associated to identities, handled by the [Name Engine](./identity/name.md)

An _identity_ is as defined in [Identity](../architecture-1/abstractions/identity.md).

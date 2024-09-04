---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Identity Machine

The identity machine is responsible for management of data and operations
related to identities, including:

- creating & deleting identities, handled by the [[Identity Management Engine]]

- encrypting to & decrypting as identities, handled by the [[Encryption Engine]]
and [[Decryption Engine]]

    - In general, a node has only one [[Encryption Engine]]
      and one [[Decryption Engine]]. Each
      [[EncryptRequest]] or [[VerifyRequest]] specifies what identity they're
      referring to.

- creating & verifying commitments, handled by the [[Commitment Engine]] and [[Verification Engine]]

  - Note that there is a [[Commitment Engine]] and/or a [[Verification Engine]]
    created on a node for each identity the node has. References to the
    [[Commitment Engine]] and/or [[Verification Engine]] can be used as a kind
    of permission, ensuring that only processes which have been given such a
    reference will be able to commit or verify with a specific identity.

- tracking relationships between identities, including

    - which identities can sign for other identities, handled by the [[Signs For Engine]]

    - which identities can read for other identities, handled by the [[Reads For Engine]]

- tracking names associated to identities, handled by the [[Name Engine]]

An _identity_ is as defined in [[Identity]].

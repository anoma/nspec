---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Identity Management Engine

The identity management engine is responsible for generating, connecting, and deleting identities. It abstracts a uniform interface over identities created with different "backends", including, for example:

- internal identities stored in local memory

- internal identities stored in a hardware device, e.g. Ledger

- internal identities stored in a browser extension

- internal identities stored in another machine accessible over the network

When an identity is generated or connected, the identity management engine does not return the internal identity directly, but rather returns handles to the corresponding commitment and decryption engine instances, which can be used to generate commitments by and decrypt data encrypted to, respectively, the internal identity (which is still kept in whatever backend is in use).

## Messages

- [GenerateIdentityRequestResponse](./generate-identity-request-response.md)

- [ConnectIdentityRequestResponse](./connect-identity-request-response.md)

- [DeleteIdentityRequestResponse](./delete-identity-request-response.md)

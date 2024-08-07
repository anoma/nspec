---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Encryption Engine

The encryption engine is responsible for encrypting messages to external
identities. It automatically uses "reads for" relationship information from the
[Reads For Engine](./../reads_for/index.md) along with caller preference information in
order to choose which identity to encrypt to.

The encryption engine is a stateless function, and calls to it do not need to be
ordered. The runtime should implement this intelligently for efficiency.

## Messages

- [EncryptRequestResponse](./encrypt_request_response.md)

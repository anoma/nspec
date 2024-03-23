# Encryption Engine

The encryption engine is responsible for encrypting messages to external identities. It automatically uses "reads for" relationship information from the [Reads For Engine](./reads-for.md) along with caller preference information in order to choose which identity to encrypt to.

The encryption engine is a stateless function, and calls to it do not need to be ordered. The runtime should implement this intelligently for efficiency.

## Messages

- [EncryptRequestResponse](./encryption/encrypt-request-response.md)
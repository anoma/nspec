# Verification Engine


The verification engine is responsible for verifying commitments made by external identities. It automatically uses "signs for" relationship information from the [Signs For Engine](./signs-for.md) along with caller preference information in order to choose how to verify a commitment.

The verification engine is a stateless function, and calls to it do not need to be ordered. The runtime should implement this intelligently for efficiency.

## Messages


- [VerifyRequestResponse](./verification/verify-request-response.md)

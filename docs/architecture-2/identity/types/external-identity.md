# ExternalIdentity

## Purpose

<!-- --8<-- [start:purpose] -->
Designates an identity in anoma. 
This could represent an internal component, or a user, or an anoma node, etc. 
The External Identity encodes all the information necessary to encrypt messages to _and_ verify commitments from some Identity represented.

This _implements_ the [External Identity Abstraction from architecture-1](../../../architecture-1/abstractions/identity.md#external-identity).
This means that, as far as our SML is concerned, we will need a `structure` matching the `EXTERNAL_IDENTITY` `signature`,  where both the `signer` and the `verifier` type are this ExternalIdentity type. 
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
There are (infinitely) many ways to make an ExternalIdentity, so this is a sum type.
Here we list _some_ of the options that should be available. 

One of:
- `ed25519`
- `secp256k1`
- `BLS`
- A [Threshold Composition](../../../architecture-1/abstractions/identity.md#threshold-composition) of External Identities.
  - This must include any information necessary about how, for example, secret sharing is done for threshold encryption.
<!-- --8<-- [end:type] -->
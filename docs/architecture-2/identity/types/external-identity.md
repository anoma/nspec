---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ExternalIdentity

## Purpose

<!-- --8<-- [start:purpose] -->
Designates an identity in Anoma. This could represent an internal component, or
a user, or an Anoma node, etc. The External Identity encodes all the information
necessary to encrypt messages to _and_ verify commitments from some Identity
represented.

This _implements_ the [[Identity#external-identity|External Identity Abstraction from]].
This means that, as far as our SML is concerned, we will need a `structure`
matching the `EXTERNAL_IDENTITY` `signature`, where both the `signer` and the
`verifier` type are this [[ExternalIdentity]] type.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
There are (infinitely) many ways to make an [[ExternalIdentity]], so this is a sum type.
Here we list _some_ of the options that should be available.

One of:

- `ed25519`
- `secp256k1`
- `BLS`
- A [[Identity#threshold-composition|Threshold Composition]] of External
  Identities.
  - This must include any information necessary about how, for example, secret
    sharing is done for threshold encryption.
<!-- --8<-- [end:type] -->

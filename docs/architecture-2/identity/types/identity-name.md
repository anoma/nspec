# IdentityName

## Purpose

<!-- --8<-- [start:purpose] -->
Serves as an alias for an [[ExternalIdentity]] in anoma.
This is useful when we do not yet have the (cryptographic) specifics for an identity, but we want to refer to it anyway.
These are resolved by the [[Name Engine]].

This _implements_ the [Identity Name Abstraction from architecture-1](../../../architecture-1/abstractions/identity.md#identity-names).
This means that, as far as our SML is concerned, we will need a `structure` matching the `VERIFIER_NAME` and `ENCRYPTOR_NAME` `signature`s,  where the `identityName` type is this IdentityName.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
There are (infinitely) many ways to make an IdentityName, so this is a sum type.
Each element also specifies here what kind of [[IdentityNameEvidence]] is necessary to prove that a given [[ExternalIdentity]] corresponds with this IdentityName, as used by the [[Name Engine]].
At the moment, we support 2 types of IdentityNames:

One of:
- `LOCAL_NAME`
  - Structure: `string`
  - [[IdentityNameEvidence]]: NONE
  - The [[Name Engine]] must known any Corresponding [[ExternalIdentity]]s at launch (from configuration). These may include, for example:
    - "localnode" representing this node's [[ExternalIdentity]]
- `DOT`
  - Structure: Pair of Parent : [[ExternalIdentity]], Child : `string`
  - [[IdentityNameEvidence]]: a signed statement from Parent designating that some [[ExternalIdentity]] corresponds to Child.
  - These implement the ["." Notation Sub-Identity abstraction](../../../architecture-1/abstractions/identity.md#-notation).
<!-- --8<-- [end:type] -->

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# IdentityNameEvidence

## Purpose

<!-- --8<-- [start:purpose] -->
Serves as evidence that an [[IdentityName]] corresponds to an [[ExternalIdentity]] in anoma.
These are stored and evaluated by the [[Name Engine]].

This _implements_ the [Evidence part of the Identity Name Abstraction from architecture-1](../../../architecture-1/abstractions/identity.md#identity-names).
This means that, as far as our SML is concerned, we will need a `structure` matching the `VERIFIER_NAME` and `ENCRYPTOR_NAME` `signature`s,  where the `evidence` type is this IdentityNameEvidence.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
There are (infinitely) many ways to make an IdentityName, and possibly different evidence for each, so this is a sum type.
Each element here corresponds to a specific element of [[IdentityName]].
At the moment, we support 1 types of IdentityNameEvidence:

One of:

- `DOT`
  - Structure a signed statement from Parent designating that some [[ExternalIdentity]] corresponds to Child.
  - These implement the ["." Notation Sub-Identity abstraction](../../../architecture-1/abstractions/identity.md#-notation).
<!-- --8<-- [end:type] -->

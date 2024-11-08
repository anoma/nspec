---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource

A **resource** is a composite structure `Resource` that contains the following components:

|Component|Type|Description|
|-|-|-|
|`logicRef`|`LogicHash`|succinct representation of the predicate associated with the resource (resource logic)|
|`labelRef`|`LabelHash`|specifies the fungibility domain for the resource. Resources within the same fungibility domain are seen as equivalent kinds of different quantities. Resources from different fungibility domains are seen and treated as distinct asset kinds. This distinction comes into play in the balance check described later|
|`valueRef`|`ValueHash`|is the fungible data associated with the resource. It contains extra information but does not affect the resource's fungibility|
|`quantity`|`Quantity`|is a number representing the quantity of the resource|
|`isEphemeral`|`Bool`|is a flag that reflects the resource's ephemerality. Ephemeral resources do not get checked for existence when being consumed|
|`nonce`|`Nonce`|guarantees the uniqueness of the resource computable components|
|`nullifierKeyCommitment`|`NullifierKeyCommitment`|is a nullifier key commitment. Corresponds to the nullifier key $nk$ used to derive the resource nullifier (nullifiers are further described [here](./computable_components/nullifier.md))|
|`randSeed`|`RandSeed`|randomness seed used to derive whatever randomness needed|

To distinguish between the resource data structure consisting of the resource components and a resource as a unit of state identified by just one (or some) of the resource computed fields, we sometimes refer to the former as a *resource plaintext*.
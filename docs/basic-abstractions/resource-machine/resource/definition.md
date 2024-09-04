---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource

A **resource** is a composite structure $R = (l, label, q, v, eph, nonce, npk, rseed): Resource$ where:

- $Resource = \mathbb{F}_{l} \times \mathbb{F}_{label} \times \mathbb{F}_Q \times \mathbb{F}_{v} \times \mathbb{F}_b \times \mathbb{F}_{nonce} \times  \mathbb{F}_{npk} \times \mathbb{F}_{rseed}$
- $l: \mathbb{F}_{l}$ is a succinct representation of the predicate associated with the resource (resource logic)
- $label: \mathbb{F}_{label}$ specifies the fungibility domain for the resource. Resources within the same fungibility domain are seen as equivalent kinds of different quantities. Resources from different fungibility domains are seen and treated as distinct asset kinds. This distinction comes into play in the balance check described later.
- $q: \mathbb{F}_Q$ is a number representing the quantity of the resource
- $v: \mathbb{F}_{v}$ is the fungible data associated with the resource. It contains extra information but does not affect the resource's fungibility
- $eph: \mathbb{F}_b$ is a flag that reflects the resource's ephemerality. Ephemeral resources do not get checked for existence when being consumed
- $nonce: \mathbb{F}_{nonce}$ guarantees the uniqueness of the resource computable components
- $npk: \mathbb{F}_{npk}$ is a nullifier public key. Corresponds to the nullifier key $nk$ used to derive the resource nullifier (nullifiers are further described [here](./computable-components/nullifier.md))
- $rseed: \mathbb{F}_{rseed}$: randomness seed used to derive whatever randomness needed

To distinguish between the resource data structure consisting of the resource components and a resource as a unit of state identified by just one (or some) of the resource computed fields, we sometimes refer to the former as a resource plaintext.
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource

_Resources_ are the atomic units of state in Anoma.

## Data structure

Define a _resource_ $R$ as a seven-tuple $(F, F, F, F, F, F, 0 | 1)$ with fields
named as follows:

- $R_{logic\_hash}$ of type $F$

- $R_{label\_hash}$ of type $F$

- $R_{quantity}$ of type $F$

- $R_{value\_hash}$ of type $F$

- $R_{nonce}$ of type $F$

- $R_{nc}$ of type $F$ ("nullifier commitment")

- $R_{ephemerality}$ of type ${ 0_P | 1_P }$

Resources are constant-size ($6F + 1$).

## Computed fields

Resources with $R_{ephemerality} = 0_P$ are known as _ephemeral_, while
resources with $R_{ephemerality} = 1_P$ are known as _persistent_.

Define the _commitment_ of a resource $R_{commitment}$ as $hash(R)$.

Define the _address_ of a resource $R_{address}$ as $R_{commitment}$.

!!! todo

     Same as the commitment for now.

Define the _nullifier_ of a resource $R_{nullifier}$ as $n$ such that $hash(n) = R_{nc}$.

Define the _kind_ of resource $R_{kind}$ as $hash(R_{logic}, R_{label})$.

Define the _delta_ of a resource $R_{delta}$ as the two-tuple $(R_{kind}, R_{quantity})$.

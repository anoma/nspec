---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Kudos

## Cryptographic Kudos

_Cryptographic kudos_ are a resource class in which every resource is associated
with the identity of the initial creator of a resource, called the _instantiator_. 
They come in fungible/non-fungible as well as transferable/non-transferable
varieties with optional additional constraints. 

Kudos enable a rich set of applications and mechanism design approaches and are
one of the core primitives of Anoma.

Example use cases: 

- For each packet $A$ routes for $B$, $B$ instantiates and transfers one kudo of the
  kind `B_routing` and transfers it to $A$, with the promise to route one packet
  for whoever offers one `B_routing` kudo.

## Kudo Kind

The kind of a kudo is determined by its *resource logic* and *label*. Different
logic components exist for fungible or non-fungible, as well as transferable or
non-transferable, leading to six different kudo logics. The label contains the
external identity of the instantiator (the initial creator of any single kudo)
and an optional suffix for the creation of different subkinds. 

## Ownership 

Each kudo has a current owner set in the value field denoted by an external
identity, which is the only identity that can authorize a transfer (see below).

## Instantiation

Any identity can act as an instantiator for all kudo kinds bound to their
identity. To instantiate a kudo, a transaction must be generated which consumes
a special resource (TBD: marked by a bitfield) that is created out of nothing,
creating a kudo with the owner set to the instantiator.

For a kudo to be valid, the logic must check for a proof of this TX to be present.

## Transfer

To transfer a kudo, the current owner of a kudo sets up a transaction consuming
the kudo and creating a new one of the same kind, placing the recipients
external identity in the owner field and signing over the resource.

During validation of a TX we check that for each resource of a certain kind that
gets created, a resource of the same kind was consumed and a signature of the
former owner exists.

### Non-Transferable Kudos

Non-transferable kudos can only be transferred a single time by the
instantiator, who is the initial owner. 

## Kudo Swaps

In the case of transferable kudos, swap intents can be formulated.
To enable solving, this can also be done with unbalanced TXs.

!!! example

  $A$ wants to route packets via $C$, but $C$ only accepts `B_routing` kudos.
  $A$ can then formulate an intent swapping any $A$-kudos, e.g. `A_routing` or
  `A_storage` kudos for `B_routing` or `C_routing` kudos.

### Solving

Solving could be performed by for example, cycle finding algorithm or SAT
solvers.
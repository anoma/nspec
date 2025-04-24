---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.notes.roles_and_requirements;
```

# Roles and requirements


The table below contains a list of resource-related roles. In the Anoma
protocol, the role of the resource creator will often be taken by a solver,
which creates additional security requirements compared to the case when
protocol users solve their own intents. Because of that, extra measures are
required to ensure reliable distribution of the information about the created
resource to the resource receiver.

|Role| Description|
|-|-|
Authorizer | approves the resource consumption on the application level. The resource logic encodes the mechanism that connects the authorizer's external identity (public key) to the decision-making process
Annuler | knows the data required to nullify a resource
Creator | creates the resource and shares the data with the receiver
Owner | can both authorize and annul a resource
Sender | owns the resources that were consumed to create the created resource
Receiver | owns the created resource

## Reliable resource object distribution

In the case of in-band distribution of created resources in contexts with higher
security requirements, the resource creator is responsible for encrypting the
resource object. Verifiable encryption must be used to ensure the correctness of
the encrypted data: the encrypted object must be proven to correspond to the
resource object, which is passed as a private input.

## Reliable nullifier key distribution

Knowing the resource’s nullifier reveals information about when the resource is
consumed, as the nullifier will be published when it happens, which might be
undesirable in the contexts with higher security requirements. For that reason,
it is advised to keep the number of parties who can compute the resource’s
nullifier as low as possible in such contexts.

In particular, the resource creator should not be able to compute the resource
nullifier, and as the nullifier key allows to compute the resource's nullifier,
it shouldn't be known to the resource creator. At the same time, the resource
object must contain some information about the nullifier key. One way to fulfil
both requirements is, instead of sharing the nullifier key itself with the
resource creator, to share some parameter derived from the nullifier key, but
that does not allow computing the nullifier key or any meaningful information
about it. This parameter is called a nullifier key commitment and is computed as
$cnk = h_{cnk}(nk)$.

> These concerns are not meaningful in the contexts with lower security
requirements.

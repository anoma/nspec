---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource logic proof

Resource logic proofs attest to validity of resource logics. A resource logic is a computable predicate associated with a resource that constrains the creation and consumption of a resource. Each time a resource is created or consumed, the corresponding resource logic proof is required in order for the action (and thus the transaction) to be valid.

## Proving

When proving, resource logics take as input resources created and consumed in the action:

#### Instance

1. [[Computable components#Tag | Resource tag]] — identifies the current resource being checked
2. `isConsumed` - a flag that tells the logic if the resource is consumed or created
3. `action.consumed` (possibly excluding the tagged resource, if it is consumed)
4. `action.created` (possibly excluding the tagged resource, if it is created)
5. `action.applicationData[tag]`

#### Witness

1. for consumed resources: `OrderedSet (Resource, NullifierKey)`
2. for created resources: `OrderedSet Resource`
3. Application inputs

!!! note
    The instance and witness values are expected to correspond to each other: the first tag in the instance corresponds to the first resource object in the witness (and corresponds to the resource being checked), and so on. Note that the tag has to be recomputed from the object to verify that it indeed corresponds to the tag (this condition is included in the constraints)

#### Constraints

1. Created commitment integrity: `r.commitment() = cm`
2. Consumed nullifier integrity: `r.nullifier(nullifierKey) = nf`
3. Application constraints
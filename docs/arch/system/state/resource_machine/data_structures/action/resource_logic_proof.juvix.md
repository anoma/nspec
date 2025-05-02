
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.action.resource_logic_proof;
```

# Resource logic proof

Resource logic proofs attest to validity of resource logics. A resource logic is a computable predicate associated with a resource (this resource is referred to as `self` in this context) that constrains the creation and consumption of a resource. Each time a resource is created or consumed, the corresponding resource logic proof is required in order for the action (and thus the transaction) to be valid.

## Proving

When proving, resource logics take as input resources created and consumed in that action.

#### Instance

1. Resource's commitment/nullifier
2. `isConsumed` - a flag that tells the logic if the resource is consumed or created
3. `consumed` (excluding the tagged resource, if it is consumed)
4. `created` (excluding the tagged resource, if it is created)
5. `applicationData`


#### Witness

1. `self` resource object
2. If `isConsumed = True`: nullifier key of `self`
3. Resource objects of consumed resources: `List (Resource, NullifierKey)`
4. Resource objects of created resources: `List Resource`
5. Application-specific inputs

!!! note
    Instance and witness elements are expected to go in the same order: the first element of the instance corresponds to the first elements of the witness and so on.

#### Constraints

1. For created resources: created commitment integrity: `r.commitment() = cm`
2. For consumed resources: `r.nullifier(nullifierKey) = nf`
3. Application-specific constraints

Checks that require access to global `CMTree` and `NullifierSet`:

1. each created resource wasn't created in prior transactions
2. each consumed resource wasn't consumed in prior transactions

!!! note
  Actions can be verified as parts of supposedly valid transactions and individually, when building a valid transaction (e.g., in the partial solving case). In case the actions are verified _not_ individually, all global checks can be aggregated and verified at once to reduce the amount of global communication.

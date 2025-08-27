
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

It is worth noting that resource logics are permissionless. The ARM, acting as the verifier, can only control the instance shape.

## Action tree

When proving, resource logics take as input resources created and consumed in that action represented by a root of a merkle tree containing the relevant resources.

#### Instance

1. Resource's commitment/nullifier
2. `isConsumed` - a flag that tells the logic if the resource is consumed or created. Can be inferred from the position of the tag in the corresponding compliance unit.
3. `actionTreeRoot`. Action tree is a Merkle tree that contains commitments and nullifiers of the action resources. The resource logic takes as input the root of the action tree.
4. `applicationData.ResourcePayload`
5. `applicationData.DiscoveryPayload`
6. `applicationData.ExternalPayload`
7. `applicationData.ApplicationPayload`

Including `applicationData` payloads in the instance requires collecting the first entry from each tuple: `List (BitString, DeletionCriterion) -> List BitString`. We assume that a proving system can differentiate between the four payloads, in partciular, given an argument from application data, the circuit can differentiate from which payload it came.

The original order of the elements must be preserved at each step.

#### Witness

!!! note

    As resource logics are permissionless, the RM does not control the possible witness structure. Nevertheless, below we provide the recommended structure for applications to support.

1. `self` resource object
2. If `isConsumed = True`: nullifier key of `self`
3. Resource objects of consumed resources: `List (Resource, NullifierKey, ActionTreePath)`
4. Resource objects of created resources: `List (Resource, ActionTreePath)`
5. Application-specific inputs


#### Constraints

!!! note

    The circuit contraints 1-3 are also recommended but ultimately can only be decided to be enforced by applications themselves.

1. For created resources: created commitment integrity: `r.commitment() = cm`
2. For consumed resources: `r.nullifier(nullifierKey) = nf`
3. Application-specific constraints

Checks that require access to global `CMTree` and `NullifierSet`:

1. each created resource wasn't created in prior transactions
2. each consumed resource wasn't consumed in prior transactions

!!! note
  Actions can be verified as parts of supposedly valid transactions and individually, when building a valid transaction (e.g., in the partial solving case). In case the actions are verified _not_ individually, all global checks can be aggregated and verified at once to reduce the amount of global communication.

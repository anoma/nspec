
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.action.index;
```

# Action

An action is a composite structure of type `Action` that contains the following components:

|Component|Type|Description|
|-|-|-|
|`resourceLogicProofs`|`Map Tag (isConsumed: Bool, RL_VK: ResourceLogicProvingSystem.VerifyingKey, applicationData: List (BitString, DeletionCriterion), proof: ResourceLogicProvingSystem.Proof, memo: BitString)`|Resource logic proofs for resources associated with the action. The key of the map is the resource for which the proof is computed. The deletion criterion field is described [[Stored data format |here]].|
|`complianceUnits`|`List ComplianceUnit`|The set of transaction's [[Compliance unit | compliance units]]|

!!! note
    For function privacy in the shielded context, instead of a logic proof we verify a proof of a logic proof validity - a recursive proof. `LogicVerifyingKeyHash` type corresponds to the RL VK commitment while verifying key in `resourceLogicProofs` refers to the key to be used for verification (i.e., verifier circuit verifying key as opposed to a resource logic verifying key). RL VK commitment should be included somewhere else, e.g., `applicationData`.

Actions partition the state change induced by a transaction and limit the resource logics evaluation context: proofs created in the context of an action have access only to the resources associated with the action. A resource is said to be *associated with an action* if its commitment or nullifier is present in the action's `created` or `consumed` correspondingly. A resource is associated with at most two actions: resource creation is associated with exactly one action and resource consumption is associated with exactly one action. A resource is said to be *consumed in the action* for a valid action if its nullifier is present in the action's `consumed` list. A resource is said to be *created in the action* for a valid action if its commitment is in the action's `created` list.

!!! note
    Unlike transactions, actions don't need to be balanced, but if an action is valid and balanced, it is sufficient to create a balanced transaction.

## Interface

1. `create(List (NullifierKey, Resource, CMtreePath, CMTreeRoot), List (BitString, DeletionCriterion))), List (Resource, List (BitString, DeletionCriterion))) -> Action`
2. `verify(Action) -> Bool`
3. `delta(Action) -> DeltaHash`


## Proofs
For each resource consumed or created in the action, it is required to provide a proof that the logic associated with that resource evaluates to `True` given the input parameters that describe the state transition induced by the action. The number of such proofs in an action equals to the amount of resources (both created and consumed) in that action, even if some resources have the same logics. Resource logic proofs are further described [[Resource logic proof | here]].

## `create`

1. `complianceUnits`: Partition the resources into compliance units and compute a compliance proof for each unit
2. `resourceLogicProofs`: For each resource, compute a resource logic proof. Associate each proof (and other components needed to verify it) with the tag of the resource

## `verify`

Validity of an action can only be determined for actions that are associated with a transaction. Assuming that an action is associated with a transaction, an action is considered valid if all of the following conditions hold:

1. All resource logic proofs associated with the action are valid
2. All compliance proofs associated with the action are valid: `cu.verify() = True for cu in complianceUnits`
3. `resourceLogicProofs` keys = the list of tags associated with `complianceUnits` (ignoring the order)

## `delta`

`action.delta() -> DeltaHash` is a computable component used to compute `transactionDelta`. It is computed from `r.delta()` of the resources that comprise the action and defined as `action.delta() = sum(cu.delta() for cu in action.complianceUnits)`.
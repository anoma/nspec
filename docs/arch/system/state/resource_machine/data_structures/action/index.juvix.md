
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
|`resourceLogicProofs`|`Map Tag (isConsumed: Bool, logicVKOuter: LogicVKOuterHash, applicationData: List (BitString, DeletionCriterion), proof: ResourceLogicProvingSystem.Proof)`|Resource logic proofs for resources associated with the action. The key of the map is the resource for which the proof is computed. The deletion criterion field is described [[Stored data format |here]].|
|`complianceUnits`|`List ComplianceUnit`|The set of transaction's [[Compliance unit | compliance units]]|

!!! note
    For function privacy in the shielded context, instead of a logic proof we verify a proof of a logic proof validity - a recursive proof. `LogicVKOuterHash` type corresponds to the RL VK commitment while verifying key in `resourceLogicProofs` refers to the key to be used for verification (i.e., verifier circuit verifying key as opposed to a resource logic verifying key). RL VK commitment should be included somewhere else, e.g., `applicationData`.

Actions partition the state change induced by a transaction and limit the resource logics evaluation context: proofs created in the context of an action have access only to the resources associated with the action. A resource is said to be *associated with an action* if its tag is present in the set of `resourceLogicProofs` keys . A resource is associated with at most two actions: resource creation is associated with exactly one action and resource consumption is associated with exactly one action. A resource is said to be *consumed in the action* for a valid action if its *nullifier* is present in the set of `resourceLogicProofs` keys. A resource is said to be *created in the action* for a valid action if its *commitment* is in the set of `resourceLogicProofs` keys.

!!! note
    Unlike transactions, actions don't need to be balanced, but if an action is valid and balanced, it is sufficient to create a balanced transaction.

## Interface

<<<<<<< HEAD
<<<<<<< HEAD
1. `create(List (NullifierKey, Resource, deltaExtraInput, CMtreePath, CMTreeRoot), List (BitString, DeletionCriterion))), List (Resource, deltaExtraInput, List (BitString, DeletionCriterion)), appWitness: BitString) -> Action`
2. `verify(Action) -> Bool`
3. `delta(Action) -> DeltaHash`
4. `to_instance(Action, Tag) -> Maybe ResourceLogicProvingSystem.Instance`
=======
1. `create(List (NullifierKey, Resource, deltaExtraInput, CMtreePath, CMTreeRoot), List (BitString, DeletionCriterion))), List (Resource, deltaExtraInput, List (BitString, DeletionCriterion))) -> Action`
=======
1. `create(List (NullifierKey, Resource, deltaExtraInput, CMtreePath, CMTreeRoot), List (BitString, DeletionCriterion))), List (Resource, deltaExtraInput, List (BitString, DeletionCriterion)), appWitness: BitString) -> Action`
>>>>>>> f76a58fd99 (Remove memo, add global check notes, more vk hashes renaming)
2. `verify(Action) -> Bool`
3. `delta(Action) -> DeltaHash`
4. `to_instance(Action, Tag) -> ResourceLogicProvingSystem.Instance`
>>>>>>> 749587b6ac (Resolve conflicts with main)


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

`action.delta()` computes the action delta. Action delta is computed from `r.delta()` of the resources that comprise the action and defined as `action.delta() = sum(cu.delta() for cu in action.complianceUnits)`.

## `to_instance`

This function assembles the instance required to verify a resource logic proof from the data in the action.

The main question to answer here is how to assemble `consumed` and `created` lists of resources. The proposed mechanism works as follows:
1. Iterate over all compliance units and accumulate the lists of created and consumed resources. The resulting list of consumed resources contains all consumed resources in the action. The resulting list of created resources contains all created resources in the action.
2. Erase the `self` resource from the relevant list. If the resource is consumed and its nullifier is stored under index `n` in the list of consumed resources, the resulting list is `l[0], l[1], ..., l[n - 1], l[n + 1], ...`. Keep the list of created resources the same.
3. If `self` is created, erase the resource from the list of created resources as in step 2. Keep the list of consumed resources the same. For each resource we assemble an instance for, we erase only one resource - itself - from one list.

!!! note
   When verifying multiple logic proofs from the same action, it might make sense to create the 'full' lists once and erase resources one at a time to create a particular instance. Note that the next instance must be created from the original `full` list, not the list with previously erased resources.

All other fields of the instance (resource tag, `isConsumed`, `applicationData`) are taken from the relevant entry of `resourceLogicProofs`.

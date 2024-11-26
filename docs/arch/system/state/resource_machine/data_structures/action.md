# Action

An action is a composite structure of type `Action` that contains the following components:

|Component|Type|Description|
|-|-|-|
|`created`|`Set Commitment`|contains commitments of resources created in this action|
|`consumed`|`Set Nullifier`|contains nullifiers of resources consumed in this action|
|`resourceLogicProofs`|`Map Tag (LogicRefHash, PS.Proof)`|contains a map of resource logic proofs associated with this action. The key is the `self` resource for which the proof is computed, the first parameter of the value opens to the required verifying key, the second one is the corresponding proof|
|`complianceUnits`|`Set ComplianceUnit`|The set of transaction's [compliance units](./compliance_unit.md)|
|`applicationData`|`Map AppDataValueHash (BitString, DeletionCriterion)`|contains a map of hashes and [openings](./../primitive_interfaces/fixed_size_type/hash.md#hash) of various data needed to verify resource logic proofs. The deletion criterion field is described [here](./../notes/storage.md#data-blob-storage). The openings are expected to be ordered.|


!!! note
    `resourceLogicProofs` type: For function privacy, we assume that the produced logic proof is recursive, and the verifying key used to verify the proof is either universal and publicly known (in case we have a recursion) - then the verifying key for the inner proof is committed to in the `LogicRefHash` parameter - or it is contained directly in the `LogicRefHash` parameter. This part isn't properly generalised yet.

!!! warning
    The key for the proof map probably shouldn't be `BitString` but I couldn't figure out the universal enough key types that can be used as a way to find all associated inputs. Perhaps using literally the same key as for `applicationData` will make it straightforward enough

Actions partition the state change induced by a transaction and limit the resource logics evaluation context: proofs created in the context of an action have guaranteed access only to the resources associated with the action. A resource is said to be *associated with an action* if its commitment or nullifier is present in the action's `created` or `consumed` correspondingly. A resource is associated with exactly one action. A resource is said to be *consumed in the action* for a valid action if its nullifier is present in the action's `consumed` set. A resource is said to be *created in the action* for a valid action if its commitment is in the action's `created` set.

## Interface

1. `createProven(Set Resource, Set Resource, ApplicationData) -> Action` - creates a proven action
2. `createUnproven(Set Commitment, Set Nullifier, ApplicationData) -> Action` - creates an unproven action
3. `delta(Action) -> DeltaHash`
4. `prove(Action, Map Tag (LogicRefHash, PS.Proof), Set (PS.VerifyingKey, PS.Instance, PS.Proof)) -> Action` - takes as input an unproven action, a set of logic proofs, and a set of compliance proofs. Outputs a proven action
5. `verify(Action) -> Bool`

## Proofs
Each action refers to a set of resources to be consumed and a set of resources to be created. Creation and consumption of a resource requires a set of proofs that attest to the correctness of the proposed action. There are two proof types associated with each action:

1. *Resource logic proofs* are created by `ResourceLogicProvingSystem`. For each resource consumed or created in the action, it is required to provide a proof that the logic associated with that resource evaluates to `True` given the input parameters that describe the state transition induced by the action. The number of such proofs in an action equals to the amount of resources (both created and consumed) in that action, even if some resources have the same logics. Resource logic proofs are further described [here](./proof/logic.md).
2. *Resource machine [compliance proofs](./action.md#compliance-proofs-and-compliance-units)* are created by `ComplianceProvingSystem`. Compliance proofs ensure that the provided action complies with the resource machine definitions. Actions are partitioned into *compliance units*, and there is one compliance proof created for each compliance unit. Compliance proofs and compliance units are further described [here](./proof/compliance.md).


## `create`

Given a set of input resource objects `consumedResources: Set (NullifierKey, Resource)`, a set of output resource plaintexts `createdResources: Set Resource`, and `applicationData`, including a set of application inputs required by resource logics, a proven action is computed the following way:

1. Compute the required resource logic and compliance proofs
2. For the compliance proofs, create a set of proof records `Set (PS.VerifyingKey, PS.Instance, PS.Proof)` and put them in `action.complianceProofs`
3. For the logic proofs, associate each proof with the logic hash reference and the tag of the resource for which the proof is created, and put the resulting map in `action.resourceLogicProofs`
4. `action.consumed = r.nullifier(nullifierKey) for r in consumedResources`
5. `action.created = r.commitment() for r in createdResources`
6. `action.applicationData = applicationData`

An unproven action would be computed the same way, except that some resource logic proofs and compliance proofs wouldn't be computed yet.

## Unproven and proven actions

An action that contains all of the [required proofs](./action.md#proofs) is considered **proven**. Such an action is bound to the resources it contains and cannot be modified without reconstructing the proofs.

In case an action doesn't contain all of the expected proofs, it is called **unproven**. Unproven actions are, strictly speaking, not valid actions (because they don't contain the required proofs), but might be handy when the proving context for the resource logics is still being constructed.

#### Unproven → proven action

After adding the required proofs to an unproven action, the action becomes proven.

## `prove`

Given the lacking compliance proofs and logic proofs in addition to action as input to the function, the resulting action is computed by adding the proofs to the relevant components:

!!! warning
    Such an update could also require an update to `applicationData` and possibly other fields. Not sure how to describe this in the most versatile way yet as it isn't clear how proving unproven actions would be used in practice

!!! warning
    Given the ability to update the data structure components, it is important to make sure the structure doesn't contain unused elements

## `verify`

Validity of an action can only be determined for actions that are associated with a transaction. Assuming that an action is associated with a transaction, an action is considered valid if all of the following conditions hold:

1. action input resources have valid resource logic proofs associated with them: `Verify(RLVerifyingKey, RLInstance, RLproof) = True`
2. action output resources have valid resource logic proofs associated with them: `Verify(RLVerifyingKey, RLInstance, RLproof) = True`
3. all compliance proofs are valid: `Verify(complianceVerifyingKey, complianceInstance, complianceProof) = True`
4. transaction's $rts$ field contains correct `CMtree` roots (that were actual `CMtree` roots at some epochs) used to [prove the existence of consumed resources](./action.md#input-existence-check) in the compliance proofs.

## Action delta (computable component)

`action.delta() -> DeltaHash` is a computable component used to compute `transactionDelta`. It is computed from `r.delta()` of the resources that comprise the action and defined as `action.delta() = sum(r.delta() for r in consumedResources) - sum(r.delta() for r in createdResources)`

From the homomorphic properties of [`DeltaHash`](./../primitive_interfaces/fixed_size_type/delta_hash.md), for the resources of the same kind $kind$, adding together the deltas of the resources results in the delta corresponding to the total quantity of that resource kind: $\sum_j{h_\Delta(kind, q_{r_{i_j}})} - \sum_j{h_\Delta(kind, q_{r_{o_j}})} = \sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}} =  h_\Delta(kind, q_{kind})$, where $q_{kind}$ is the total quantity of the resources of kind $kind$.

The kind-distinctness property of $h_\Delta$ allows computing $\Delta_{tx} = \sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}}$ adding resources of all kinds together without the need to account for distinct resource kinds explicitly: $\sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}} = \sum_j{h_\Delta(kind_j, q_{kind_j})}$.


!!! note
    When action delta is provided as input and not computed directly, it has to be explicitly checked that the action delta is correctly computed from the resource deltas.

!!! note
    Unlike transactions, actions don't need to be balanced, but if an action is valid and balanced, it is sufficient to create a balanced transaction.

## Action composition

Since proven actions already contain all of the required proofs, there is no need to expand the evaluation context of such actions, therefore *proven actions are not composable*.

Right now we assume that each action is created by exactly one party in one step, meaning that *unproven actions are not composable*.
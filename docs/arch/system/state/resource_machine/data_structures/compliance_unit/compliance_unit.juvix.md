---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.compliance_unit.compliance_unit;
```

# Compliance unit

`ComplianceUnit` is a data structure that partitions the [[Action | action]], meaning that there might be multiple compliance units for a single action, the sets of resources covered by any two compliance units cover don't intersect, and together the compliance units cover all of the resources in the action. This partition corresponds to the format expected by the compliance proving system used to produce compliance proofs. The table below describes the components of a compliance unit:

|Component|Type|Description|
|-|-|-|
|`vk`|`ComplianceProvingSystem.VerifyingKey`|
|`instance`|`ComplianceProvingSystem.Instance`|The instance required to verify the compliance proof. Includes the tags of the checked resources, compliance unit delta, `CMtree` roots for consumed resources.|
|`proof`| `ComplianceProvingSystem.Proof`||

The number of created and consumed resources in each unit is determined by the resource machine *instantiation*. The total number of compliance proofs required for an action is determined by the number of compliance units that comprise the action. For example, if the instantiation defines a single compliance proof to include 1 input and 1 output resource, and an action contains 3 input and 2 output resources, the total number of compliance units will be 3 (with a placeholder output resource in the third compliance unit).

## Interface

1. `create(ComplianceProvingSystem.ProvingKey, ComplianceProvingSystem.VerifyingKey, ComplianceProvingSystem.Instance, ComplianceProvingSystem.Witness) -> ComplianceUnit` - computes the compliance unit proof and populates the compliance unit
2. `created(ComplianceUnit) -> List Commimtent` - returns the commitments of the created resources checked in the unit
3. `consumed(ComplianceUnit) -> List Nullifier` - returns the nullifiers of the consumed resources checked in the unit
4. `verify(ComplianceUnit) -> Bool` - returns `ComplianceProvingSystem.Verify(vk, instance, proof)`
5. `delta(ComplianceUnit) -> DeltaHash` - returns the compliance unit delta, which is stored in `complianceData`: `unit.delta() = unit.complianceData.delta`

### `create`

Create is a function that provers use to create a compliance unit.

1. Compute the compliance proof: `ComplianceProvingSystem.Prove(ComplianceProvingSystem.ProvingKey, ComplianceProvingSystem.Instance, ComplianceProvingSystem.Witness) -> ComplianceProvingSystem.Proof`. What comprises the instance and witness here is described in [[Compliance proof]].
2. Create the compliance unit given the proof, verifying key, and instance.

### Delta

Compliance unit delta is used to compute action and transaction deltas and is itself computed from resource deltas: `delta = sum(r.delta() for r in outputResources - sum(r.delta() for r in inputResources))`. Note that the delta is computed by the prover (who knows the resource objects of resources associated with the unit) and is a part of the instance. The compliance proof must ensure the correct computation of delta from the resource deltas available at the proving time.

#### Delta for computing balance

From the homomorphic properties of [[Delta hash]], for the resources of the same kind $kind$, adding together the deltas of the resources results in the delta corresponding to the total quantity of that resource kind: $\sum_j{h_\Delta(kind, q_{r_{i_j}})} - \sum_j{h_\Delta(kind, q_{r_{o_j}})} = \sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}} =  h_\Delta(kind, q_{kind})$, where $q_{kind}$ is the total quantity of the resources of kind $kind$.

The kind-distinctness property of $h_\Delta$ allows computing $\Delta = \sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}}$ adding resources of all kinds together without the need to account for distinct resource kinds explicitly: $\sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}} = \sum_j{h_\Delta(kind_j, q_{kind_j})}$.

As a result, the properties of `DeltaHash` allow computing the total balance for a compliance unit, action, or transaction, without having direct access to quantities and kinds of the resources that comprise the data structure.

### `verify`

1. `ComplianceProvingSystem.Verify(vk, instance, proof) = True`
2. Global check: `CMTree` roots used to verify the proof are valid `CMTree` roots

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.compliance_unit;
```

# Compliance proofs and compliance units

`ComplianceUnit` is a data structure that partitions the [action](./action.md),
meaning that there might be multiple compliance units for a single action, the
sets of resources covered by any two compliance units cover don't intersect, and
together the compliance proofs cover all of the resources in the action. This
partition corresponds to the format expected by the compliance proving system
used to produce compliance proofs. The table below describes the components of a
compliance unit:

|Component|Type|Description|
|-|-|-|
|`proof`| `PS.Proof`||
|`refInstance`|`ReferencedInstance`|The instance required to verify the compliance proof. Includes the references to the tags of the checked resources, compliance unit delta, `CMtree` roots references|
|`vk`|`PS.VerifyingKey`|

!!! warning

    `ReferenceInstance` is a modified `PS.Instance` structure in which some
        elements are replaced by their references. To get `PS.Instance` from
        `ReferencedInstance` the referenced structures must be dereferenced. The
    structures we assume to be referenced here are: - CMtree roots (stored in
    transaction) - commitments and nullifiers (stored in action) All other
    instance elements are assumed to be as the instance requires.

!!! note

    Referencing Merkle tree roots: the Merkle tree roots required to verify the
    compliance proofs are stored in the transaction (not in action or a
    compliance unit), and are referenced by a short hash in `refInstance`. To
    find the right roots corresponding to the proof, the verifier has to compute
    the hashes of the roots in the transaction, match them with the short hashes
    in the `refInstance` structure, and use the ones that match for
    verification. A similar approach is used to reference the tags of the
    checked in the compliance unit resources.


The size of a compliance unit - the number of created and consumed resources in
each unit - is determined by the resource machine *instantiation*. The total
number of compliance proofs required for an action is determined by the number
of compliance units that comprise the action. For example, if the instantiation
defines a single compliance proof to include 1 input and 1 output resource, and
an action contains 3 input and 2 output resources, the total number of
compliance units will be 3 (with a placeholder output resource in the third
compliance unit).

## Delta

Compliance unit delta is used to compute action and transaction deltas and is
itself computed from resource deltas: `delta = sum(r.delta() for r in
outputResources - sum(r.delta() for r in inputResources))`. Note that the delta
is computed by the prover (who knows the resource objects of resources
associated with the unit) and is a part of the instance. The compliance proof
must ensure the correct computation of delta from the resource deltas available
at the proving time.

#### Delta for computing balance

From the homomorphic properties of
[`DeltaHash`](./../primitive_interfaces/fixed_size_type/delta_hash.md), for the
resources of the same kind $kind$, adding together the deltas of the resources
results in the delta corresponding to the total quantity of that resource kind:
$\sum_j{h_\Delta(kind, q_{r_{i_j}})} - \sum_j{h_\Delta(kind, q_{r_{o_j}})} =
\sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}} =  h_\Delta(kind,
q_{kind})$, where $q_{kind}$ is the total quantity of the resources of kind
$kind$.

The kind-distinctness property of $h_\Delta$ allows computing $\Delta =
\sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}}$ adding resources of all
kinds together without the need to account for distinct resource kinds
explicitly: $\sum_j{\Delta_{r_{i_j}}} - \sum_j{\Delta_{r_{o_j}}} =
\sum_j{h_\Delta(kind_j, q_{kind_j})}$.

As a result, the properties of `DeltaHash` allow computing the total balance for
a compliance unit, action, or transaction, without having direct access to
quantities and kinds of the resources that comprise the data structure.

## Interface

1. `delta(ComplianceUnit) -> DeltaHash` - returns the compliance unit delta, which is stored in `complianceData`: `unit.delta() = unit.complianceData.delta`
2. `created(ComplianceUnit) -> Set Commimtent` - returns the commitments of the created resources checked in the unit
3. `consumed(ComplianceUnit) -> Set Nullifier` - returns the nullifiers of the consumed resources checked in the unit
4. `create(PS.ProvingKey, PS.Instance, PS.Proof) -> ComplianceUnit` - computes the compliance proof and stores the data (or references to it, if stored elsewhere) required to verify it in the compliance unit
4. `verify(ComplianceUnit) -> Bool` - returns `ComplianceProvingSystem.Verify(vk, instance, proof)`, where `instance` is computed from `refInstance` by dereferencing
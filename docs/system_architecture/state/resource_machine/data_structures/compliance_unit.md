# Compliance proofs and compliance units

`ComplianceUnit` is a data structure that partitions the [action](./action.md), meaning that there might be multiple compliance units for a single action, the sets of resources covered by any two compliance units cover don't intersect, and together the compliance proofs cover all of the resources in the action. This partition corresponds to the format expected by the compliance proving system used to produce compliance proofs. The table below describes the components of a compliance unit:

|Component|Type|Description|
|-|-|-|
|`proof`| `PS.Proof`||
|`refInstance`|`ReferencedInstance`|The instance required to verify the compliance proof. Includes the references to the tags of the checked resources, compliance unit delta, `CMtree` roots references|
|`vk`|`PS.VerifyingKey`|

!!! warning
    `ReferenceInstance` is a modified `PS.InStance` structure in which some elements replaced by their references. To get `PS.Instance` from `ReferencedInstance` the referenced structures should be dereferenced. The structures we assume to be referenced here are:
        - CMtree roots (stored in transaction)
        - commitments and nullifiers (stored in action)
    All other instance elements are assumed to be as the instance requires.

!!! note
    Referencing Merkle tree roots: the Merkle tree roots required to verify the compliance proofs are stored in the transaction (not in action or a compliance unit), and are referenced by a short hash in `refInstance`. To find the right roots corresponding to the proof, the verifier has to compute the hashes of the roots in the transaction, match them with the short hashes in the `refInstance` structure, and use the ones that match for verification. A similar approach is used to reference the tags of the checked in the compliance unit resources.


The size of a compliance unit - the number of created and consumed resources in each unit - is determined by the resource machine *instantiation*. The total number of compliance proofs required for an action is determined by the number of compliance units that comprise the action. For example, if the instatiation defines a single compliance proof to include 1 input and 1 output resource, and an action contains 3 input and 2 output resources, the total number of compliance units will be 3 (with a placeholder output resource in the third compliance unit).

## Interface

1. `delta(ComplianceUnit) -> DeltaHash` - returns the compliance unit delta, which is stored in `complianceData`: `unit.delta() = unit.complianceData.delta`
2. `created(ComplianceUnit) -> Set Commimtent` - returns the commitments of the created resources checked in the unit
3. `consumed(ComplianceUnit) -> Set Nullifier` - returns the nullifiers of the consumed resources checked in the unit
# Compliance proofs and compliance units

`ComplianceUnit` is a data structure that partitions the [action](./action.md), meaning that there might be multiple compliance units for a single action, the sets of resources covered by any two compliance units cover don't intersect, and together the compliance proofs cover all of the resources in the action. This partition corresponds to the format expected by the compliance proving system used to produce compliance proofs. The table below describes the components of a compliance unit:

|Component|Type|Description|
|-|-|-|
|`created`|`Set Resource`|a subset of the action created resources|
|`consumed`|`Set Resource`|a subset of the action consumed resources|

The size of a compliance unit is determined by the resource machine *instantiation*. The total number of compliance proofs required for an action is determined by the number of compliance units that comprise the action. For example, if the instatiation defines a single compliance proof to include 1 input and 1 output resource, and an action contains 3 input and 2 output resources, the total number of compliance units will be 3 (with a placeholder output resource in the third compliance unit).

!!! note
    Compliance unit is not included in the transaction directly (as it consists of resource objects), but is used to create compliance proofs included in the [action](./action.md#proofs). Compliance unit is a data structure that is only available to the prover.

## Interface

1. `prove(ComplianceUnit) -> (PS.Proof, PS.Instance)` - for a given compliance unit, computes and fetches (if necessary) the required inputs from the storage, passes them to the compliance proving system, outputting a compliance proof along with the instance required to verify the proof.
2. `delta(ComplianceUnit) -> DeltaHash` - computes the compliance unit delta: `unit.delta() = sum(r.delta() for r in unit.consumed) - sum(r.delta() for r in unit.created)`
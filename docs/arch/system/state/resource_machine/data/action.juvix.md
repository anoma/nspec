---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data.action;
import prelude open;
```

# `Action`

An *action* is a term of type `Action` defined as follows:

```juvix
type Action :=
  mkAction@{
    -- created : List (TODO "Commitment");
    -- consumed : List (TODO "Nullifier");
    -- resourceLogicProofs : Map (TODO "Tag") (TODO "LogicRefHash, PS.Proof");
    -- complianceUnits : Set (TODO "ComplianceUnit");
    -- applicationData : Map (TODO "AppDataValueHash") (TODO "BitString, DeletionCriterion");
  };
```

???+ quote "Arguments"

    `created`
    : contains commitments of resources created in this action

    `consumed`
    : contains nullifiers of resources consumed in this action

    `resourceLogicProofs`
    : contains a map of resource logic proofs associated with this action. The
    key is the `self` resource for which the proof is computed, the first
    parameter of the value opens to the required verifying key, the second one is
    the corresponding proof

    `complianceUnits`
    : The set of transaction's compliance units

    `applicationData`
    : contains a map of hashes and [openings](./../primitive_interfaces/fixed_size_type/hash.md#hash) of various
    data needed to verify resource logic proofs. The deletion criterion field is
    described [here](./../notes/storage.md#data-blob-storage). The openings are
    expected to be ordered

!!! note `resourceLogicProofs` type: For function privacy, we assume that the
    produced logic proof is recursive, and the verifying key used to verify the
    proof is either universal and publicly known (in case we have a recursion) -
    then the verifying key for the inner proof is committed to in the
    `LogicRefHash` parameter - or it is contained directly in the `LogicRefHash`
    parameter. This part isn't properly generalised yet.

Actions partition the state change induced by a transaction and limit the
resource logics evaluation context: proofs created in the context of an action
have access only to the resources associated with the action. A resource is said
to be *associated with an action* if its commitment or nullifier is present in
the action's `created` or `consumed` correspondingly. A resource is associated
with exactly one action. A resource is said to be *consumed in the action* for a
valid action if its nullifier is present in the action's `consumed` list. A
resource is said to be *created in the action* for a valid action if its
commitment is in the action's `created` list.

!!! note Unlike transactions, actions don't need to be balanced, but if an
    action is valid and balanced, it is sufficient to create a balanced
    transaction.

## Interface

1. `create(Set (NullifierKey, Resource), Set Resource, ApplicationData) ->
Action` - creates an action 2. `delta(Action) -> DeltaHash` 3. `verify(Action)
-> Bool`

## Proofs Each action refers to a set of resources to be consumed and a set of
resources to be created. Creation and consumption of a resource requires a set
of proofs that attest to the correctness of the proposed action. There are two
proof types associated with each action:

1. *Resource logic proofs* are created by `ResourceLogicProvingSystem`. For each
resource consumed or created in the action, it is required to provide a proof
that the logic associated with that resource evaluates to `True` given the input
parameters that describe the state transition induced by the action. The number
of such proofs in an action equals to the amount of resources (both created and
consumed) in that action, even if some resources have the same logics. Resource
logic proofs are further described [here](./proof/logic.md). 2. *Resource
machine [compliance proofs](./action.md#compliance-proofs-and-compliance-units)*
are created by `ComplianceProvingSystem`. Compliance proofs ensure that the
provided action complies with the resource machine definitions. Actions are
partitioned into *compliance units*, and there is one compliance proof created
for each compliance unit. Compliance proofs and compliance units are further
described [here](./proof/compliance.md).

## `create`

Given a set of input resource objects `consumedResources: Set (NullifierKey,
Resource, CMtreePath)`, a set of output resource plaintexts `createdResources:
Set Resource`, and `applicationData`, including a set of application inputs
required by resource logics, an action is computed the following way:

1. Partition action into compliance units and compute a compliance proof for
each unit. Put the information about the units in `action.complianceUnits` 2.
For each resource, compute a resource logic proof. Associate each proof with the
tag of the resource and the logic hash reference. Put the resulting map in
`action.resourceLogicProofs` 3. `action.consumed = r.nullifier(nullifierKey) for
r in consumedResources` 4. `action.created = r.commitment() for r in
createdResources` 5. `action.applicationData = applicationData`

## `verify`

Validity of an action can only be determined for actions that are associated
with a transaction. Assuming that an action is associated with a transaction, an
action is considered valid if all of the following conditions hold:

1. action input resources have valid resource logic proofs associated with them:
`verify(RLVerifyingKey, RLInstance, RLproof) = True` 2. action output resources
have valid resource logic proofs associated with them: `verify(RLVerifyingKey,
RLInstance, RLproof) = True` 3. all compliance proofs are valid:
`complianceUnit.verify() = True` 4. transaction's $rts$ field contains correct
`CMtree` roots (that were actual `CMtree` roots at some epochs) used to [prove
the existence of consumed resources](./action.md#input-existence-check) in the
compliance proofs.

## `delta`

`action.delta() -> DeltaHash` is a computable component used to compute `transactionDelta`. It is computed from `r.delta()` of the resources that comprise the action and defined as `action.delta() = sum(cu.delta() for cu in action.complianceUnits)`.
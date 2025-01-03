
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - action
  - transaction
  - resource-machine
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.action;
    import prelude open;
    import arch.system.types.nullifier open;
    import arch.system.types.commitment open;
    ```

# Actions

An *action* is a term of type `Action` that represent *atomic transactions* or
*state changes*.

## Purpose

Actions are atomic units of [[State|state]] change within a
[[Transaction|transaction]]. They serve the following main purposes.

1. **State Change Organization**: Actions partition a transaction's overall
state change into smaller, focused units. Each action clearly specifies which
resources are being created and consumed by the associated [[Transaction|transaction]].

2. **Proof Context Isolation**: Actions provide an isolated context for
[[Resource logic proof|resource logic proofs]]. When evaluating proofs for a
resource, only the resources associated with that action are accessible. This
isolation helps manage complexity and ensures proper resource handling.

### Resource Association

We also need to discuss how resources are associated with actions.

A resource can be associated with an action in two ways:

- Through its corresponding [[Commitment|commitment]] in the action's `created`
field, indicating it is being created 

- Through its corresponding [[Nullifier|nullifier]] in the action's `consumed`
field, indicating it is being consumed

Important properties of this resource association:

- Resources listed in `consumed` are considered "consumed in the action".
- Resources listed in `created` are considered "created in the action".
- Each resource is associated with exactly one action in case it is created or
consumed in the action.

Now we can define the `Action` type.

## `Action`

A *transaction action* or simply *action* is a term of type `Action`.

```juvix
type Action A := mkAction {
  created : Set (Commitment A);
  consumed : Set Nullifier;
  -- resourceLogicProofs : Map Tag (LogicRefHash, PS.Proof);
  -- complianceUnits : Set ComplianceUnit;
  -- applicationData : Map Tag (BitString, DeletionCriterion);
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
    parameter of the value opens to the required verifying key, the second one
    is the corresponding proof

    `complianceUnits`
    : The set of transaction's [[Compliance unit| compliance units]]

    `applicationData`
    : maps tags to relevant application data needed to verify resource logic
    proofs. The deletion criterion field is described [[Stored data format
    |here]]. The openings are expected to be ordered.

??? quote "Auxiliary Juvix code: Instances"

    ```juvix
    deriving
    instance
    eqAction {A} {{Eq A}}: Eq (Action A);
    ```

    ```juvix
    deriving
    instance
    ordAction {A} {{Ord A}}: Ord (Action A);
    ```


## Properties

### A resource can only be associated with one action when being consumed or
created

### Actions must provide proofs for all *resource transitions*

<!--

!!! note

    `resourceLogicProofs` type: For function privacy, we assume that the
    produced logic proof is recursive, and the verifying key used to verify the
    proof is either universal and publicly known (in case we have a recursion) -
    then the verifying key for the inner proof is committed to in the
    `LogicRefHash` parameter - or it is contained directly in the `LogicRefHash`
    parameter. This part isn't properly generalised yet.


!!! note

    Unlike transactions, actions don't need to be balanced, but if an action is
    valid and balanced, it is sufficient to create a balanced transaction.

## Interface

```juvix
-- axiom
-- create
--   (nfs : Set (NullifierKey, Resource))
--   (created : Set Resource)
--   (applicationData : ApplicationData) -> Action;

-- axiom
-- delta (action : Action) -> DeltaHash;

-- axiom
-- verify (action : Action) -> Bool;
```


## Proofs

For each resource consumed or created in the action, it is required to provide a
proof that the logic associated with that resource evaluates to `True` given the
input parameters that describe the state transition induced by the action. The
number of such proofs in an action equals to the amount of resources (both
created and consumed) in that action, even if some resources have the same
logics. Resource logic proofs are further described [[Resource logic proof |
here]].

## `create`

Given a set of input resource objects `consumedResources: Set (NullifierKey,
Resource, CMtreePath)`, a set of output resource plaintexts `createdResources:
Set Resource`, and `applicationData`, including a set of application inputs
required by resource logics, an action is computed the following way:

1. Partition action into compliance units and compute a compliance proof for
each unit. Put the information about the units in `action.complianceUnits`

2. For each resource, compute a resource logic proof. Associate each proof with
the tag of the resource and the logic hash reference. Put the resulting map in
`action.resourceLogicProofs`

3. `action.consumed = r.nullifier(nullifierKey) for r in consumedResources`

4. `action.created = r.commitment() for r in createdResources`

5. `action.applicationData = applicationData`

## `verify`

Validity of an action can only be determined for actions that are associated
with a transaction. Assuming that an action is associated with a transaction, an
action is considered valid if all of the following conditions hold:

1. action input resources have valid resource logic proofs associated with them:
`verify(RLVerifyingKey, RLInstance, RLproof) = True`

2. action output resources have valid resource logic proofs associated with
them: `verify(RLVerifyingKey, RLInstance, RLproof) = True`

3. all compliance proofs are valid: `complianceUnit.verify() = True`

4. transaction's $rts$ field contains correct `CMtree` roots (that were actual
`CMtree` roots at some epochs) used to prove the existence of consumed resources
in the compliance proofs.

## `delta`

`action.delta() -> DeltaHash` is a computable component used to compute
`transactionDelta`. It is computed from `r.delta()` of the resources that
comprise the action and defined as `action.delta() = sum(cu.delta() for cu in
action.complianceUnits)`.

-->
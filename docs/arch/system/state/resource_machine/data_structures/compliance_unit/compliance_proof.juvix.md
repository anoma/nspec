---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.compliance_unit.compliance_proof;
```

# Compliance proof

Compliance proofs are created by `ComplianceProvingSystem` and computed over compliance units. Compliance proofs ensure that the provided state transition complies with the resource machine definitions.

## Compliance inputs

#### Instance

|Name|Type|Description|
|-|-|-|
|`consumed`|`List (nf: Nullifier, root: CMTree.Value, logicVKOuter: LogicVKOuterHash)`|Each entry corresponds to a consumed resource and includes a hash of the resource's [[Resource | `logicRef` component]]|
|`created`|`List (cm: Commitment, logicVKOuter: LogicVKOuterHash)`|Each entry corresponds to a created resource|
|`unitDelta`|`DeltaHash`||

#### Witness

1. for consumed resources:

    1. resource object `r`

    2. `nullifierKey`

    3. `CMtree` path to the consumed resource commitment

    4. pre-image of `logicVKOuter`

    5. `deltaExtraInput` used to compute resource delta

2. for created resources:

  1. resource object `r`

  2. pre-image of `logicVKOuter`

  3. `deltaExtraInput` used to compute resource delta

!!! note

    Instance and witness elements are expected to go in the same order: the first element of the instance corresponds to the first (4 for consumed and 2 for created) elements of the witness and so on.

## Compliance constraints
Each resource machine compliance proof must check the following:

1. Merkle path validity: `CMTree::Verify(r.commitment(), path, root) = True` for each resource associated with a nullifier from the `consumed`. For ephemeral resources a "fake" relation is checked.

2. For each consumed resource `r`:

  1. Nullifier integrity: `r.nullifier(nullifierKey) is in consumed`
  2. Logic integrity: `logicVKOuter = logicVKOuterHash(r.logicRef, ...)`

3. For each created resource `r`:

  1. Commitment integrity: `r.commitment() is in created`
  2. Logic integrity: `logicVKOuter = logicVKOuterHash(r.logicRef, ...)`

4. Delta integrity: `unitDelta = sum(r.delta(deltaExtraInput(r)) for r in consumed) - sum(r.delta(deltaExtraInput(r)) for r in created)` where `deltaExtraInput(r)` returns `deltaExtraInput` associated with resource `r`

!!! note
    Kind integrity is checked implicitly in delta integrity

!!! note
    [2.3, 3.2]: Combined with checking the logic proofs, logic integrity checks allow to ensure that the logics associated with the resources are satisfied

!!! note
    [2.1, 3.1]: To ensure correct binding between the instance and the witness, resource tags have to be recomputed from the witness and compared to what is provided in the instance.

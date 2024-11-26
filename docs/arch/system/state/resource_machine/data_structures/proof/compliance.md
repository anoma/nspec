Compliance proofs are computed over [compliance units](./../compliance_unit.md).

## Compliance inputs

#### Instance

1. tags of all of the resources in the compliance unit
2. roots for the consumed non-ephemeral resources in the compliance unit
3. unit delta
4. commitments to `logicRef` resource components (used for referencing the `logicRef` without explicitly using the component value) `logicRefHash`

#### Witness

1. resource objects of all resources in the compliance unit
2. paths for each consumed non-ephemeral resource
3. consumed resource commitment
4. nullifier keys for consumed resources
5. opening of `logicRefHash`

!!! note
    The instance and witness values are expected to correspond to each other: the first tag in the instance corresponds to the first resource object in the witness, and so on. Note that the tag has to be recomputed from the object to verify that it indeed corresponds to the tag (included in the constraints)

## Compliance constraints
Each resource machine compliance proof must check the following:

1. each *non-ephemeral* consumed resource was created: for each resource associated with a nullifier from the `consumedResourceTagSet`: `CMTree::Verify(cm, path, root) = True`
2. the resource commitments and nullifiers are derived according to the commitment and nullifier derivation rules (including the commitments of the consumed resources):
  1. for each consumed resource `r`: 
    1. `r.nullifier(nullifierKey) is in consumedResourceTagSet`
    2. `r.commitment() = cm` 
  2. for each created resource `r`: 
    1. `r.commitment() is in createdResourceTagSet` 
3. delta of the unit is computed correctly
4. the verifying keys used to verify the logic proofs are the same keys that the resources are associated with (`logicRef` component). Together with checking the logic proofs (separately) allows to ensure the logics associated with the resources are satisfied


!!! note
    to ensure correct computation of a commitment/nullifier, they have to be recomputed from the raw parameters (resource object and possibly `nullifierKey`) and compared to what is provided in the tag set.

Compliance proofs must be composition-independent: composing two actions, the compliance proof sets can be simply united to provide a valid composed action compliance proof set.
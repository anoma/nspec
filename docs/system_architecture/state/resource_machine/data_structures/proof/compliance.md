Compliance proofs are computed over [compliance units](./../compliance_unit.md).

## Compliance inputs

#### Instance

- tags of all of the resources in the compliance unit
- roots for the consumed non-ephemeral resources in the compliance unit
- unit delta
- commitments to `logicRef` resource components (used for referencing the `logicRef` without explicitly using the component value) `logicRefCommitment`

#### Witness

- resource plaintexts of all resources in the compliance unit
- paths for each consumed non-ephemeral resource
- consumed resource commitment
- nullifier keys for consumed resources
- opening of `logicRefCommitment` 

## Compliance constraints
Each resource machine compliance proof must check the following:

- each *non-ephemeral* consumed resource was created: for each resource associated with a nullifier from the `consumedResourceTagSet`: `CMTree::Verify(cm, path, root) = True`
- the resource commitments and nullifiers are derived according to the commitment and nullifier derivation rules (including the commitments of the consumed resources):
  - for each consumed resource `r`: 
    - `r.nullifier(nullifierKey) is in consumedResourceTagSet`
    - `r.commitment() = cm` 
  - for each created resource `r`: 
    - `r.commitment() is in createdResourceTagSet` 
- delta of the unit is computed correctly
- the resource logics of created and consumed resources are satisfied


!!! note
    to ensure correct computation of a commitment/nullifier, they have to be recomputed from the raw parameters (resource plaintext and possibly `nullifierKey`) and compared to what is provided in the tag set.

Compliance proofs must be composition-independent: composing two actions, the compliance proof sets can be simply united to provide a valid composed action compliance proof set.

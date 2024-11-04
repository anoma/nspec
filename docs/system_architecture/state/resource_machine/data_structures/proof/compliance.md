# Compliance proofs and compliance units

The size of a compliance unit is determined by the resource machine *instantiation*. The total number of compliance proofs required for an action is determined by the number of compliance units that comprise the action. For example, if the instatiation defines a single compliance proof to include 1 input and 1 output resource, and an action contains 3 input and 2 output resources, the total number of compliance units will be 3 (with a "dummy" output resource in the third compliance unit).

## Compliance inputs

#### Instance

TODO

#### Witness

TODO

## Compliance constraints
Each resource machine compliance proof must check the following:

- each *non-ephemeral* consumed resource was created: for each resource associated with a nullifier from the `consumedResourceTagSet`: `CMTree::Verify(cm, path, root) = True`
- the resource commitments and nullifiers are derived according to the commitment and nullifier derivation rules (including the commitments of the consumed resources):
  - for each consumed resource `r`: 
    - `r.nullifier(nullifierKey) is in consumedResourceTagSet`
    - `r.commitment() = cm` (`cm` for the consumed resource is provided as a part of witness)
  - for each created resource `r`: 
    - `r.commitment() is in createdResourceTagSet` 
- resource deltas are computed correctly
- the resource logics of created and consumed resources are satisfied

!!! note
    to ensure correct computation of a commitment/nullifier, they have to be recomputed from the raw parameters (resource plaintext and possibly `nullifierKey`) and compared to what is provided in the tag set.

Compliance proofs must be composition-independent: composing two actions, the compliance proof sets can be simply united to provide a valid composed action compliance proof set.

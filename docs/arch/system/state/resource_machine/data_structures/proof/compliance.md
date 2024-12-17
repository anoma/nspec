---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Compliance proof

Compliance proofs are computed over [compliance units](./../compliance_unit.md).
<!--ᚦ
    «Can we summarize the data that we "actually need" here (as a prover)?
»--><!--ᚦ
    «Each compliance unit seems to have a set of resources associated with it,
    aech of which is either consumed or produced...I guess.
    This all should become clear already in this intro.»
--><!--ᚦ
    «@over ?
    what depends on what?
    it seems that compliance units make reference to
    compliance input data fields?»
--><!--ᚦ
    «add description along the lines:
    we want to create a proof using a witness and an instance»
-->


## Compliance inputs

<!--ᚦ
    «Inputs, to what? the prover, or which function?»
--><!--ᚦ
    «Btw, often there seems to be "consumed resource"="input resource"»
-->


#### Instance

|Name|Type|Description|
|-|-|-|
|`consumed`|`List (NullifierRef, RootRef, LogicRefHash)`|Includes nullifiers' references of all consumed resources in the compliance unit, root references, and commitments to [`logicRef` resource components](./../resource/definition.md) (used for referencing the `logicRef` without explicitly using the component value) for consumed resources|<!--ᚦ« what is "component value" mean here?»-->
|`created`|`List (CommitmentRef, LogicRefHash)`|Commitments' references of all created resources in the compliance unit|
|`unitDelta`|`DeltaHash`|Unit delta|<!--ᚦ«DeltaHash.T as the type»--><!--ᚦ«add description: sum of all deltas in the unit, *hashed*»-->

#### Witness

1. for consumed resources:
    1. resource object
    2. nullifier key
    3. CMtree path
    4. resource commitment
    5. opening of `logicRefHash` (implicitly includes `logicRef` - already included as a part of the resource object - and other data used to derive `logicRefHash`, e.g., randomness)
2. for created resources:
    1. resource object
    2. opening of `logicRefHash`

<!--ᚦ
    «All of these should be wiki-linked.»
-->

!!! note

    The instance and witness values are expected to correspond to each other: the first tag in the instance corresponds to the first resource object in the witness, and so on. Note that in the compliance proof, the tag is recomputed from the object to verify that the tag is correct
    <!--ᚦ
        «Can we spell this out in more detail,
        making reference to `consumed` and `created` lists?
        Or are we talking about other lists?
        »
    -->

## Compliance constraints
Each resource machine compliance proof must check the following:

1. Merkle path validity (for *non-ephemeral* resources only): `CMTree::Verify(cm, path, root) = True` for each resource associated with a nullifier from the `consumedResourceTagSet`
2. for each consumed resource `r`:
    1. Nullifier integrity: `r.nullifier(nullifierKey) is in consumedResourceTagSet`
    2. Consumed commitment integrity: `r.commitment() = cm`
    3. Logic integrity: `logicRefHash = hash(r.logicRef, ...)`
3. for each created resource `r`:
    1. Commitment integrity: `r.commitment() is in createdResourceTagSet`
    2. Logic integrity: `logicRefHash = hash(r.logicRef, ...)`
4. Delta integrity: `unitDelta = sum(r.delta() for r in consumed) - sum(r.delta() for r in created)`

!!! note
    Kind integrity is checked implicitly in delta checks

<!--ᚦ
    «@"Kind integrity" What is kind integrity?»
-->

!!! note
    [2.3, 3.2]: Combined with checking the logic proofs, logic integrity checks allow to ensure that the logics associated with the resources are satisfied

!!! note
    [2.1, 3.1]: To ensure correct computation of a commitment/nullifier, they have to be recomputed from the raw parameters (resource object and possibly `nullifierKey`) and compared to what is provided in the public tag set.

Compliance proofs must be composition-independent: composing two actions, the compliance proof sets can be simply united to provide a valid composed action compliance proof set.


<!--ᚦtags:nits,improvable-->

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Action

An action is a composite structure $A = (cms, nfs, \Pi, app\_data)$, where:

- $cms \subseteq  \mathbb{F}_{cm}$ is a set of created resources' commitments.
- $nfs \subseteq \mathbb{F}_{nf}$ is a set of consumed resources' nullifiers.
- $\Pi: \{ \pi: PS.Proof\}$ is a set of proofs.
- $app\_data: \{(k, (d, deletion\_criterion)): k \in \mathbb{F}_{key}, d \subseteq \mathbb{F}_{d}\}$ contains application-specific data needed to create resource logic proofs. The deletion criterion field is described [here](./rm_def/storage.md#data-blob-storage).

Actions define the proof context: a proof created in the context of an action assumed to have guaranteed access only to the resources associated with the action. A resource is said to be *associated with an action* if resource's commitment or nullifier is present in the action's $cms$ or $nfs$ correspondingly. A resource is said to be *consumed in the action* for a valid action if its nullifier is present in the action's $nfs$ set. A resource is said to be *created in the action* for a valid action if its commitment is present in the action's $cms$ set.

## Proofs
Each action refers to a set of resources to be consumed and a set of resources to be created. Creation and consumption of a resource requires a set of proofs that attest to the correctness of the proposed action. There are two proof types associated with each action:

- Resource logic proof $\pi_{RL}$. For each resource consumed or created in the action, it is required to provide a proof that the logic of the resource evaluates to $1$ given the input parameters that describe the state transition induced by the action (the exact resource machine instantiation [defines the exact set of parameters](./function_formats/resource_logic.md)). The number of such proofs in an action equals to the amount of resources (both created and consumed) in that action, even if the resources have the same logic.
- Resource machine [compliance proofs](./action.md#compliance-proofs-and-compliance-units) - a set of proofs that ensures that the provided action complies with the resource machine definitions.


#### Compliance proofs and compliance units

Each compliance proof maps to some *compliance unit*. The set of resources in each action is implicitly partitioned into compliance units, the size of a single compliance unit is determined by a concrete resource machine instantiation. The total number of compliance proofs required for an action is determined by the number of compliance units that comprise the action, and can vary from 1 (one proof for all resources in the action at the same time) to the total number of resources in the action (one compliance proof per one resource). For example, if the instatiation defines a single compliance proof to include 1 input and 1 output resource, and an action contains 3 input and 2 output resources, the total number of compliance units will be 3 (the third output resource can be "dummy").

###### Input existence check
Each resource machine compliance proof must check the following:

- each consumed resource was created (its commitment is included in $CMtree$)
- the resource commitments and nullifiers are derived according to the commitment and nullifier derivation rules (including the commitments of the consumed resources)
- resource deltas are computed correctly
- the resource logics of created and consumed resources are satisfied


Compliance proofs must be composition-independent: composing two actions, the compliance proof sets can be simply united to provide a valid composed action compliance proof set.

## Creation

Given a set of input resource plaintexts $\{r_{{in}_1}, \cdots, r_{{in}_n}\}$, a set of output resource plaintexts $\{r_{{out}_1}, \cdots, r_{{out}_m}\}$, a set of nullifier keys corresponding to the input resources $\{nk_1,\cdots,nk_n\}$, $app\_data$, and a set of custom inputs required by resource logics, an action $A$ is computed as:

- $cms = \{h_{cm}(r_{{out}_i}, i = 1 \cdots m\}$
- $nfs = \{h_{nf}(nk_i, r_{{in}_i}), i = 1 \cdots n\}$
- $\Pi$:
    $\{\pi_{RL}^{{in}_i}, i = 1 \cdots n \} \cup \{\pi_{RL}^{{out}_i}, i = 1 \cdots m \} \cup \{\pi_{compl}^j, 1 \leq j \leq m + n \}$
- $app\_data$

## Composition

Given two actions $a_1$ and $a_2$, their composition is computed as follows:

- $cms = cms_1 \sqcup cms_2$
- $nfs = nfs_1 \sqcup nfs_2$
- $\Pi$:
    - $\{\pi_{RL}^{{in}_i}, i = 1 \cdots n_a \} \cup \{\pi_{RL}^{{out}_i}, i = 1 \cdots m_a \} \cup \Pi_{compl_1} \cup \Pi_{compl_2}$
- $app\_data = app\_data_1 \cup app\_data_2$


The old resource logic proofs are no longer valid since the proofs context changed, new resource logic proofs must be created. The old compliance proofs are still valid.


 > Composing sets with disjoint union operator $\sqcup$, it has to be checked that those sets do not have any elements in common. Otherwise, the actions cannot be composed.


## Validity

Validity of an action cannot be determined for actions that are not associated with some transaction. Assuming that an action is associated with a transaction, an action is considered valid if the following holds:

- action input resources have valid resource logic proofs associated with them
- action output resources have valid resource logic proofs associated with them
- all compliance proofs are valid
- transaction's $rts$ field contains valid roots used to [prove the existence of consumed resources](./action.md#input-existence-check) in the compliance proofs.



> It must also be checked that the created resource was created exactly once and the consumed resource was consumed exactly once. These checks are performed separately from the checks above, given read access to the $CMtree$ and $NFset$ (a proving system is not expected to have access to these components).


## Unproven actions

An action structure that contains all of the [required proofs](./action.md#proofs) is considered proven. Such an action is bound to the resources it contains and cannot be modified without reconstructing the proofs.

In case an action cannot be proven yet or is expected to be modified, the action is called unproven. Unproven actions are not valid actions, but might be handy when the proving context for the resource logics is still being constructed. Composition for unproven actions works the same way as for proven actions except that the proofs don't need to be recomputed: there were no proofs in the first place. Once the the context is finalised, the proofs must be created for an action to become proven and valid.
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction

## Preliminaries

### Deletion criterion

Data blob storage stores data without preserving any specific structure. The data is represented as a variable length byte array and comes with a deletion criterion that determines for how long the data will be stored. The deletion criterion, in principle, is an arbitrary predicate, which in practice currently is assumed to be instantiated by one of the following options:

- delete immediately after $transaction$
- delete after $block$
- delete after $timestamp$
- delete after $sig$ over $data$
- delete after either predicate $p_1$ or $p_2$ is true; the predicates are instantiated by options from this list
- store forever

### Information flow control predicate

In principle, the information flow predicate can be arbitrary as long as it satisfies the defined signature, but for now we define a set of allowed options to instantiate the IFC predicate as $BasePredicate: BaseData -> IFCPredicate$, where $BaseData$ can be:

- $AllowAny$ - always returns 1
- $AllowOnly (Set\ ExternalIdentity)$ - returns 1 for the specified set of identities
- $RequireShielded (Set\ Hash)$ - returns 1 if the transaction doesn't contain the specified set of hashes in its fields
- $And (Set\ Predicate)$ - returns 1 when all of the specified predicates (instantiated by one of the base predicates) are satisfied
- $Or (Set\ Predicate)$ - returns 1 when at least one of the specified predicates (instantiated by one of the base predicates) is satisfied

## Core data structure

A transaction is a composite structure $TX = (rts, cms, nfs, \Pi, \Delta, extra, \Phi)$, where:

- $rts \subseteq \mathbb{F}_{rt}$ is a set of roots of $CMtree$
- $cms \subseteq  \mathbb{F}_{cm}$ is a set of created resources' commitments. 
- $nfs \subseteq \mathbb{F}_{nf}$ is a set of consumed resources' nullifiers.
- $\Pi: \{ \pi: ProofRecord\}$ is a set of proof records.
- $\Delta_{tx}: \mathbb{F}_{\Delta}$ is computed from $\Delta$ parameters of created and consumed resources. It represents the total delta change induced by the transaction.
- $extra: \{(k, (d, deletion\_criterion)): k \in \mathbb{F}_{key}, d \subseteq \mathbb{F}_{d}\}$ contains extra information requested by the logics of created and consumed resources.
- $\Phi: PREF$ where $PREF = TX \rightarrow [0, 1]$ is a preference function that takes a transaction as input and outputs a normalised value in the interval $[0,1]$ that reflects the users' satisfaction with the produced transaction. For example, a user who wants to receive at least $q=5$ of resource of kind A for a fixed amount of resource of kind B might set the preference function to implement a linear function that returns $0$ at $q=5$ and returns $1$ at $q = q_{max} = |\mathbb{F}_q| - 1$.
- $IFCPpredicate: TX \rightarrow ExternalIdentity \rightarrow \mathbb{F}_2$ is a predicate that specifies the transaction visibility.

## Operations

### Composition

Having two transactions $tx_1$ and $tx_2$, their composition $tx_1 \circ tx_2$ is defined as a transaction $tx$, where:

- $rts_{tx} = rts_1 \cup rts_2$
- $cms_{tx} = cms_1 \sqcup cms_2$
- $nfs_{tx} = nfs_1 \sqcup nfs_2$
- Proofs:
    - delta proof: $\Pi^{\Delta}_{tx} = AGG(\Pi^{\Delta}_1, \Pi^{\Delta}_2$), where $AGG$ is an aggregation function s.t. for $bv_1$ being the balancing value of the first delta proof, $bv_2$ being the balancing value of the second delta proof, and $bv_{tx}$ being the balancing value of the composed delta proof, it satisfies $bv_{tx} = bv_1 + bv_2$. The aggregation function takes two delta proofs as input and outputs a delta proof.
    - resource logic proofs: $\Pi^{RL}_{tx} = \Pi^{RL}_1 \sqcup \Pi^{RL}_2$
    - compliance proofs: $\Pi^{compl}_{tx} = \Pi^{compl}_1 \sqcup \Pi^{compl}_2$
- $\Delta_{tx} = \Delta_1 + \Delta_2$
- $extra_{tx} = extra_1 \cup extra_2$
- $\Phi_{tx} = G(\Phi_1, \Phi_2)$, where $G: PREF \times PREF \rightarrow PREF$, and $G$ is a preference function composition function
- $IFCPredicate_{tx} = IFCPredicate_1 ^ IFCPredicate_2$

!!! note

    Composing sets with disjoint union operator $\sqcup$, it has to be checked that those sets do not have any elements in common. Otherwise, the transactions cannot be composed.

## Properties

### Balance

$\Delta_{tx}$ of a transaction is computed from the delta parameters of the resources (\ref{delta-resource}) consumed and created in the transaction. It represents the total quantity change per resource kind induced by the transaction which is also referred to as \textit{transaction balance}. 

From the homomorphic properties of $h_\Delta$, for the resources of the same kind $kind$: $\sum_j{h_\Delta(kind, r_{i_j}.q)} - \sum_j{h_\Delta(kind, r_{o_j}.q)} = \sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta} =  h_\Delta(kind, q_{kind})$. The kind-distinctness property of $h_\Delta$ allows to compute $\Delta_{tx} = \sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta}$ adding resources of all kinds together without the need to explicitly distinguish between the resource kinds: $\sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta} = \sum_j{h_\Delta(kind_j, q_{kind_j})}$

### Validity

A transaction is considered _valid_ if the following statements hold:

- $rts$ contains valid $CMtree$ roots that are correct inputs for the membership proofs
- input resources have valid resource logic proofs and the compliance proofs associated with them
- output resources have valid resource logic proofs and the compliance proofs associated with them
- $\Delta$ is computed correctly and its opening is equal to the balancing value for that transaction
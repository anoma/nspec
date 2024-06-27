---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction

A **transaction** is a composite structure $TX = (rts, cms, nfs, \Pi, \Delta, extra, \Phi)$, where:

- $rts \subseteq \mathbb{F}_{rt}$ is a set of roots of $CMtree$
- $cms \subseteq  \mathbb{F}_{cm}$ is a set of created resources' commitments. 
- $nfs \subseteq \mathbb{F}_{nf}$ is a set of consumed resources' nullifiers.
- $\Pi: \{ \pi: ProofRecord\}$ is a set of proof records.
- $\Delta_{tx}: \mathbb{F}_{\Delta}$ is computed from $\Delta$ parameters of created and consumed resources. It represents the total delta change induced by the transaction.
- $extra: \{(k, (d,$ `deletion_criterion`$)): k \in \mathbb{F}_{key}, d \subseteq \mathbb{F}_{d}\}$ contains extra information requested by the logics of created and consumed resources. The deletion criterion field is described in \ref{data-blob}.
- $\Phi: PREF$ where $PREF = TX \rightarrow [0, 1]$ is a preference function that takes a transaction as input and outputs a normalised value in the interval $[0,1]$ that reflects the users' satisfaction with the produced transaction. For example, a user who wants to receive at least $q=5$ of resource of kind A for a fixed amount of resource of kind B might set the preference function to implement a linear function that returns $0$ at $q=5$ and returns $1$ at $q = q_{max} = |\mathbb{F}_q| - 1$.
- `IFCPpredicate`: `TX` $\rightarrow$ `ExternalIdentity` $\rightarrow \mathbb{F}_2$ is a predicate that specifies the transaction visibility.
    
## Information flow control

The transaction visibility specified by the `IFCpredicate` describes what parties are and are not allowed to process the transaction. In the current version it is assumed that every node is following the policy and enforcing the conditions specified by the predicate.

#### Predicate options

In principle, the information flow predicate can be arbitrary as long as it satisfies the defined signature, but for now we define a set of allowed options to instantiate the IFC predicate as `BasePredicate`: `BaseData` $\rightarrow$ `IFCPredicate`, where `BaseData` can be:

- `AllowAny` - always returns 1
- `AllowOnly (Set ExternalIdentity)` - returns 1 for the specified set of identities
- `RequireShielded (Set Hash)` - returns 1 if the transaction doesn't contain the specified set of hashes in its fields
- `And (Set Predicate)` - returns 1 when all the specified predicates (instantiated by one of the base predicates) are satisfied
- `Or (Set Predicate)` - returns 1 when at least one of the specified predicates (instantiated by one of the base predicates) is satisfied

## Transaction balance change

$\Delta_{tx}$ of a transaction is computed from the delta parameters of the resources (\ref{delta-resource}) consumed and created in the transaction. It represents the total quantity change per resource kind induced by the transaction which is also referred to as \textit{transaction balance}. 

From the homomorphic properties of $h_\Delta$, for the resources of the same kind $kind$: $\sum_j{h_\Delta(kind, r_{i_j}.q)} - \sum_j{h_\Delta(kind, r_{o_j}.q)} = \sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta} =  h_\Delta(kind, q_{kind})$. The kind-distinctness property of $h_\Delta$ allows computing $\Delta_{tx} = \sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta}$ adding resources of all kinds together without the need to explicitly distinguish between the resource kinds: $\sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta} = \sum_j{h_\Delta(kind_j, q_{kind_j})}$

> Only transactions with $\Delta_{tx}$ committing to $0$ (or any other balancing value specified by the system) can be executed and settled.

## Proofs

Each transaction refers to a set of resources to be consumed and a set of resources to be created. Creation and consumption of a resource requires a set of proofs that attest to the correctness of the proposed state transition. There are three proof types associated with a transaction:

- *Resource logic proof* $\pi_{RL}$. For each resource consumed or created in a transaction, it is required to provide a proof that the logic of the resource evaluates to $1$ given the input parameters that describe the state transition (the exact resource machine instantiation defines the exact set of parameters).
- A *delta proof* (balance proof) $\pi_{\Delta}$ makes sure that $\Delta_{tx}$ is correctly derived from $\Delta$ parameters of the resources created and consumed in the transaction and commits to the expected publicly known value, called a \textit{balancing value}. 
- A *resource machine compliance proof* $\pi_{compl}$ is required to ensure that the provided transaction is well-formed. The resource machine compliance proof must check that each consumed resource was consumed strictly after it was created, that the resource commitments and nullifiers are derived according to the commitment and nullifier derivation rules, and that the resource logics of created and consumed resources are satisfied.

> It must also be checked that the created resource was created exactly once and the consumed resource was consumed exactly once. These checks can be performed separately, with read access to the $CMtree$ and $NFset$.
#####
>Every proof is created with a proving system $PS$ and has the type $PS.Proof$. The proving system might differ for different proof types.
#####   
> For privacy-preserving contexts, all proving systems in use should support data privacy, and the proving system used to create resource logic proofs should provide function privacy in addition to data privacy: provided proofs of two different resource logics, an observer should not be able to tell which proof corresponds to which logic. It is a stronger requirement compared to data privacy, which implies that an observer does not know the private input used to produce the proof.

## Composition

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

> Composing sets with disjoint union operator $\sqcup$, it has to be checked that those sets do not have any elements in common. Otherwise, the transactions cannot be composed.

## Validity

A transaction is considered *valid* if the following statements hold:

- $rts$ contains valid $CMtree$ roots that are correct inputs for the membership proofs
- input resources have valid resource logic proofs and the compliance proofs associated with them
- output resources have valid resource logic proofs and the compliance proofs associated with them
- $\Delta$ is computed correctly, and its opening is equal to the balancing value for that transaction

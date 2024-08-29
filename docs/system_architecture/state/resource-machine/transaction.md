---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction

A transaction is a necessary and sufficient collection of fields required to apply a state update to the state.
It is a composite structure $TX = (rts, actions, \Delta, \pi_{\Delta})$, where:

- $rts \subseteq \mathbb{F}_{rt}$ is a set of roots of $CMtree$.
- $actions: \{a: Action\}$ - a set of actions.
- $\Delta_{tx}: \mathbb{F}_{\Delta}$ is computed from $\Delta$ parameters of the actions in that transaction. It represents the total quantity change per resource kind induced by the transaction, which is also referred to as \textit{transaction balance}.
- $\Pi_{\Delta}$ - transaction balance proof. It makes sure that $\Delta_{tx}$ is correctly derived from actions $\Delta$ and commits to the expected publicly known value, called a \textit{balancing value}. There is just one delta proof per transaction.


## Creation
Given a set of $CMtree$ roots $rts$ and a set of actions $actions$, $tx = (rts, actions, \pi_{\Delta}, \Delta_{tx})$, where:

- $rts = rts$
- $actions = actions$
- $\pi_{\Delta_{tx}}$
- $\Delta_{tx} = \sum{r^{in}.\Delta} - \sum{r^{out}.\Delta}$, where $r^{in}$ and $r^{out}$ correspond to the resources created and consumed in the transaction's actions

## Composition

Having two transactions $tx_1$ and $tx_2$, their composition $tx_1 \circ tx_2$ is defined as a transaction $tx$, where:

- $rts_{tx} = rts_1 \cup rts_2$
- $actions_{tx} = actions_1 \cup actions_2$
- $\Pi^{\Delta}_{tx} = AGG(\Pi^{\Delta}_1, \Pi^{\Delta}_2$), where $AGG$ is a delta proof aggregation function, s.t. for $bv_1$ being the balancing value of the first delta proof, $bv_2$ being the balancing value of the second delta proof, and $bv_{tx}$ being the balancing value of the composed delta proof, it satisfies $bv_{tx} = bv_1 + bv_2$. The aggregation function takes two delta proofs as input and outputs a delta proof. The aggregation function is defined by the proving system and might require creation of a new proof.
- $\Delta_{tx} = \Delta_1 + \Delta_2$

## Validity

A transaction is considered _valid_ if the following statements hold:

- all actions in the transaction are valid, as defined per [action validity rules](./action.md#validity)
- $\Delta$ proof is valid.


Only transactions with $\Delta_{tx}$ committing to the expected by the system balancing value can be executed.


## Transaction with Metadata

Transaction with metadata is a data structure that contains a transaction, the executable part, and metadata used by actors to make more informed decisions and enforce some policies: $TransactionWithMetadata = (Transaction, Metadata)$.

Architecture-level $Metadata$ components:

- $\Phi: PREF$ where $PREF = TX \rightarrow [0, 1]$ is a preference function that takes a transaction as input and outputs a normalised value in the interval $[0,1]$ that reflects the users' satisfaction with the given transaction. For example, a user who wants to receive at least $q=5$ of resource of kind A for a fixed amount of resource of kind B might set the preference function to implement a linear function that returns $0$ at $q=5$ and returns $1$ at $q = q_{max} = |\mathbb{F}_q| - 1$.
- $IFCPredicate: TX \rightarrow ExternalIdentity \rightarrow \mathbb{F}_2$ is a predicate that specifies the transaction visibility.

A concrete resource machine instantiation might require more $Metadata$ components.

#### Information flow control

The transaction visibility specified by the $IFCPredicate$ describes what parties are and are not allowed to process the transaction. In the current version it is assumed that every node is following the policy and enforcing the conditions specified by the predicate.

In principle, the information flow predicate can be arbitrary as long as it satisfies the defined signature, but for now we define a set of allowed options to instantiate the IFC predicate as $BasePredicate: BaseData \rightarrow IFCPredicate$, where $BaseData$ can be:

- $AllowAny$ - always returns 1
- $AllowOnly (Set\ ExternalIdentity)$ - returns 1 for the specified set of identities
- $RequireShielded (Set\ Hash)$ - returns 1 if the transaction does not contain the specified set of hashes in its fields
- $And (Set\ Predicate)$ - returns 1 when all the specified predicates (instantiated by one of the base predicates) are satisfied
- $Or (Set\ Predicate)$ - returns 1 when at least one of the specified predicates (instantiated by one of the base predicates) is satisfied

#### Composing transactions with metadata

When transactions with $Metadata$ are composed, transactions are composed according to the [transaction composition rules](./transaction.md#composition), and $MetaData$ fields are composed as follows:

- $\Phi_{tx} = G(\Phi_1, \Phi_2)$, where $G: PREF \times PREF \rightarrow PREF$, and $G$ is a preference function composition function
- $IFCPredicate_{tx} = IFCPredicate_1 \wedge IFCPredicate_2$


## Transaction function

A transaction function is a function that outputs a transaction: $TransactionFunction: () \rightarrow Transaction$.

Transaction functions take no input but can perform I/O operations to read information about global state either by reading data at the specified global storage address or by fetching data by index. The requirements for transaction functions are further described [here](./function-formats/transaction-function.md).

## Transaction balance change

$\Delta_{tx}$ of a transaction is computed from the [delta parameters of the resources](./resource/computable-components/delta.md) consumed and created in the transaction. It represents the total quantity change per resource kind induced by the transaction which is also referred to as *transaction balance*.

From the homomorphic properties of $h_\Delta$, for the resources of the same kind $kind$:
$\sum_j{h_\Delta(kind, r_{i_j}.q)} - \sum_j{h_\Delta(kind, r_{o_j}.q)} =$

$=\sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta} = h_\Delta(kind, q_{kind})$.

The kind-distinctness property of $h_\Delta$ allows computing $\Delta_{tx} = \sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta}$ by adding resources of all kinds together without the need to explicitly distinguish between the resource kinds: $\sum_j{r_{i_j}.\Delta} - \sum_j{r_{o_j}.\Delta} = \sum_j{h_\Delta(kind_j, q_{kind_j})}$

> Only transactions with $\Delta_{tx}$ committing to $0$ (or any other balancing value specified by the system) can be executed and settled.
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
- $\Delta_{tx}: \mathbb{F}_{\Delta}$ is computed from $\Delta$ parameters of the actions in that transaction. It represents the total quantity change per resource kind induced by the transaction, which is also referred to as _transaction balance_.
- $\Pi_{\Delta}$ - transaction balance proof. It makes sure that $\Delta_{tx}$ is correctly derived from actions $\Delta$ and commits to the expected publicly known value, called a _balancing value_. There is just one delta proof per transaction.


## Creation
Given a set of $CMtree$ roots $rts$ and a set of actions $actions$, $tx = (rts, actions, \pi_{\Delta}, \Delta_{tx})$, where:

- $rts = rts$
- $actions = actions$
- $\pi_{\Delta_{tx}}$
- $\Delta_{tx} = $\Delta_{tx} = \sum{a.\Delta}, a \in actions$

## Composition

Having two transactions $tx_1$ and $tx_2$, their composition $tx_1 \circ tx_2$ is defined as a transaction $tx$, where:

- $rts_{tx} = rts_1 \cup rts_2$
- $actions_{tx} = actions_1 \cup actions_2$
- $\Pi^{\Delta}_{tx} = AGG(\Pi^{\Delta}_1, \Pi^{\Delta}_2$), where $AGG$ is a delta proof aggregation function, s.t. for $bv_1$ being the balancing value of the first delta proof, $bv_2$ being the balancing value of the second delta proof, and $bv_{tx}$ being the balancing value of the composed delta proof, it satisfies $bv_{tx} = bv_1 + bv_2$. The aggregation function takes two delta proofs as input and outputs a delta proof. The aggregation function is defined by the proving system and might require creation of a new proof.
- $\Delta_{tx} = \Delta_1 + \Delta_2$

> When composing transactions, action sets are simply united without [composing the actions](./action.md#composition). For example, composing a transaction with two actions and another transaction with three actions will result in a transaction with five actions.

## Validity

A transaction is considered _valid_ if the following statements hold:

Checks that do not require access to global structures:
- all actions in the transaction are valid, as defined per [action validity rules](./action.md#validity)
- actions partition the state change induced by the transaction:
  - there is no resource created more than once across actions
  - there is no resource consumed more than once across actions
- $\pi_\Delta$ is valid

Checks that require access to global $CMtree$ and $NFset$:
- each created resource wasn't created in prior transactions
- each consumed resource wasn't consumed in prior transactions

A transaction is *executable* if it is valid and $\Delta_{tx}$ commits to the expected balancing value.

## Transaction function

A transaction function is a function that outputs a transaction: $TransactionFunction: () \rightarrow Transaction$.

Transaction functions take no input but can perform I/O operations to read information about global state either by reading data at the specified global storage address or by fetching data by index. The requirements for transaction functions are further described [here](./function_formats/transaction_function.md).
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction

A transaction is a necessary and sufficient collection of fields required to apply a state update to the state.
It is a composite structure that contains the following components:

|Component|Type|Description|
|-|-|-|
|`CMTreeRoots`|`Set CMtree.Value`|A set of valid commitment tree roots used to prove the existence of the resources being consumed in the transaction. This set is not a part of actions to avoid duplication of data|
|`actions`|`Set Action`|A set of actions that comprise the transaction|
|`transactionDelta`|`DeltaHash.T`|Transaction delta. It is computed from delta parameters of actions in that transaction. It represents the total quantity change per resource kind induced by the transaction, which is also referred to as _transaction balance_|
|`deltaProof`|`DeltaProvingSystem.Proof`|Balance proof. It makes sure that `transactionDelta` is correctly derived from the actions' deltas and commits to the expected publicly known value, called a _balancing value_. There is just one delta proof per transaction|

## Interface

- `create(Set CMtree.Value, Set Actions) -> Transaction`
- `compose(Transaction, Transaction) -> Transaction`
- `verify(Transaction) -> Bool`

## `create`
Given a set of roots and a set of actions, a transaction is formed as follows:

- `tx.CMTreeRoots = CMTreeRoots`
- `tx.actions = actions`
- `tx.transactionDelta = sum(action.Delta() for action in actions)`
- `tx.deltaProof = DeltaProvingSystem(deltaProvingKey, deltaInstance, deltaWitness)`


## `compose`

Having two transactions `tx1` and `tx2`, their composition `compose(tx1, tx2)` is defined as a transaction `tx`, where:

- `tx.CMTreeRoots = Set.union(tx1.CMTreeRoots, tx2.CMTreeRoots)`
- `tx.actions = Set.union(tx1.actions, tx2.actions)`
- `tx.deltaProof = DeltaProvingSystem.aggregate(tx1.deltaProof, tx2.deltaProof)`
- `tx.transactionDelta = tx1.transactionDelta + tx2.transactionDelta`

!!! note
    When composing transactions, action sets are simply united without [composing the actions themselves](./action.md#composition). For example, composing a transaction with two actions and another transaction with three actions will result in a transaction with five actions.

## `verify`

A transaction is considered _valid_ if the following statements hold:

Checks that do not require access to global structures:

- all actions in the transaction are valid, as defined per [action validity rules](./action.md#validity)
- actions partition the state change induced by the transaction:
  - there is no resource created more than once across actions
  - there is no resource consumed more than once across actions
- `deltaProof` is valid

Checks that require access to global $CMtree$ and $NFset$:

- each created resource wasn't created in prior transactions
- each consumed resource wasn't consumed in prior transactions

A transaction is *executable* if it is valid and `transactionDelta` commits to the expected balancing value.
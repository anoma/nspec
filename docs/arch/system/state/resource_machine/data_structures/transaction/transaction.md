---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction

A transaction is a necessary and sufficient collection of fields required to validate and apply a state update to the state.
It is a composite structure that contains the following components:

|Component|Type|Description|
|-|-|-|
|`CMTreeRoots`|`Set CMtree.Value`|A set of valid commitment tree roots used to prove the existence of the resources being consumed in the transaction. This set is not a part of actions to avoid duplication of data|
|`actions`|`Set Action`|A set of actions that comprise the transaction|
|`deltaProof`|`DeltaProvingSystem.Proof`|Balance proof. It makes sure that `transactionDelta` is correctly derived from the actions' deltas and commits to the expected publicly known value, called a _balancing value_. There is just one delta proof per transaction|

## Interface

1. `create(Set CMtree.Value, Set Actions) -> Transaction`
2. `compose(Transaction, Transaction) -> Transaction`
3. `verify(Transaction) -> Bool`
4. `delta(Transaction) -> DeltaHash`

## `create`
Given a set of roots and a set of actions, a transaction is formed as follows:

1. `tx.CMTreeRoots = CMTreeRoots`
2. `tx.actions = actions`
3. `tx.transactionDelta = sum(action.Delta() for action in actions)`
4. `tx.deltaProof = DeltaProvingSystem(deltaProvingKey, deltaInstance, deltaWitness)`


## `compose`

Having two transactions `tx1` and `tx2`, their composition `compose(tx1, tx2)` is defined as a transaction `tx`, where:

1. `tx.CMTreeRoots = Set.union(tx1.CMTreeRoots, tx2.CMTreeRoots)`
2. `tx.actions = Set.union(tx1.actions, tx2.actions)`
3. `tx.deltaProof = DeltaProvingSystem.aggregate(tx1.deltaProof, tx2.deltaProof)`
4. `tx.transactionDelta = tx1.transactionDelta + tx2.transactionDelta`

!!! note
    When composing transactions, action sets are simply united without [composing the actions themselves](./action.md#composition). For example, composing a transaction with two actions and another transaction with three actions will result in a transaction with five actions.

## `verify`

A transaction is considered _valid_ if the following statements hold:

Checks that do not require access to global structures:

1. all actions in the transaction are valid, as defined per [action validity rules](./action.md#validity)
1. actions partition the state change induced by the transaction:
  1. there is no resource created more than once across actions
  2. there is no resource consumed more than once across actions
3. `deltaProof` is valid

Checks that require access to global `CMTree` and `NullifierSet`:

1. each created resource wasn't created in prior transactions
2. each consumed resource wasn't consumed in prior transactions

A transaction is *executable* if it is valid and `transactionDelta` commits to the expected balancing value.

## `delta`

Transaction delta is computed from delta parameters of actions in that transaction. It represents the total quantity change per resource kind induced by the transaction, which is also referred to as _transaction balance_.

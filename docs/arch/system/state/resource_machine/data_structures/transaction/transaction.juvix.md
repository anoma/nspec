---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.transaction.transaction;
```

# Transaction

A transaction is a necessary and sufficient collection of fields required to validate and apply a state update to the state.
It is a composite structure that contains the following components:

|Component|Type|Description|
|-|-|-|
|`actions`|`Set Action`|A set of actions that comprise the transaction|
|`deltaProof`|`DeltaProvingSystem.Proof`|Balance proof. It makes sure that `transactionDelta` is correctly derived from the actions' deltas and commits to the expected publicly known value, called a _balancing value_. There is just one delta proof per transaction|
|`delta_vk`| `DeltaProvingSystem.VerifyingKey`|Used to verify the delta proof. Might be optional in case the key is computable from other components|
|`expectedBalance`| Balanced transactions have delta pre-image 0 for all involved kinds, for unbalanced transactions `expectedBalance` is a non-zero value.

## Interface

1. `create(Set Actions, DeltaProvingSystem.ProvingKey, DeltaProvingSystem.Instance, DeltaProvingSystem.Witness) -> Transaction`
2. `compose(Transaction, Transaction) -> Transaction`
3. `verify(Transaction) -> Bool`
4. `delta(Transaction) -> DeltaHash`

## `create`
Given a set of actions alongside delta data a transaction is formed as follows:

1. `tx.actions = actions`
2. `tx.deltaProof = DeltaProvingSystem.Prove(DeltaProvingSystem.ProvingKey, DeltaProvingSystem.Instance, DeltaProvingSystem.Witness)`

## `compose`

Having two transactions `tx1` and `tx2`, their composition `compose(tx1, tx2)` is defined as a transaction `tx`, where:

2. `tx.actions = Set.union(tx1.actions, tx2.actions)`
3. `tx.deltaProof, tx.delta_vk = DeltaProvingSystem.aggregate(tx1.deltaProof, tx1.delta_vk, tx2.deltaProof, tx2.delta_vk)`

!!! note
    When composing transactions, action sets are simply united. For example, composing a transaction with two actions and another transaction with three actions will result in a transaction with five actions, given all actions are distinct.

## `verify`

A transaction is considered _valid_ if the following statements hold:

Checks that do not require access to global structures:

1. all actions in the transaction are valid, as defined per [[Action#`verify` | action validity rules]]
1. actions partition the state change induced by the transaction:
  1. there is no resource created more than once across actions
  2. there is no resource consumed more than once across actions
3. `deltaProof` is valid

A transaction is *executable* if it is valid and `transactionDelta` commits to the expected balancing value.

## `delta`

Transaction delta is a hash of _transaction balance_ - the total quantity change per resource kind induced by the transaction. It isn't computed from the transaction balance directly by applying a hash function to it, but rather by using the homomoprhic properties of `deltaHash`: adding action deltas together results in transaction delta.
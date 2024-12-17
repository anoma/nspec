---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transaction

A transaction is a necessary and sufficient collection of fields required to validate and apply a state update to the state.<!--ᚦ
    «We may want to have a footnote explaining that
    ---as discussed on several occasions---
    there seems to be a clash between
      - transaction (as short hand for transaction object,
        i.e., object of the class/interface `Transaction`)
      - the usage of the term `transaction` in OLTPs
        https://en.wikipedia.org/wiki/Online_transaction_processing#Meaning_of_the_term_transaction,
        where it roughly means "state update"»
--><!--ᚦ
    «If this clash is real,
    we may want to use sth. like "transaction object"
    whenever the need to disabiguate arises.»
--><!--ᚦ
    «Who is in charge of applying the state update (typically)?
    The controler, right?»
--><!--ᚦ
    «How is the state update applied?
    This should be something involving updating
    nullifier set,
    commitment sets
    (and state roots?).»
-->
It is a composite structure that contains the following components:

|Component|Type|Description|
|-|-|-|
|`CMTreeRoots`|`Set CMtree.Value`|A set of valid commitment tree roots used to prove the existence of the resources being consumed in the transaction. This set is not a part of actions to avoid duplication of data|
|`actions`|`Set Action`|A set of actions that comprise the transaction|
|`transactionDelta`|`DeltaHash.T`|Transaction delta. It is computed from delta parameters of actions in that transaction. It represents the total quantity change per resource kind induced by the transaction, which is also referred to as _transaction balance_|
|`deltaProof`|`DeltaProvingSystem.Proof`|Balance proof. It makes sure that `transactionDelta` is correctly derived from the actions' deltas and commits to the expected publicly known value, called a _balancing value_. There is just one delta proof per transaction|


<!--ᚦ
    «@"delta parameters"
    "paramters"→"values"?»
--><!--ᚦ
    «"transaction balance" is probably the better name (compared to delta)
    -- it would be nice if we were consistent»
--><!--ᚦ
    «@CMTreeRoots: Why not more general, e.g., a set of AccumulatorValue ?»
--><!--ᚦ
    «@comprise
    The sentence "A set of actions that comprise the transaction" sounds to me
    as if there was nothing else but actions in a _transaction object_»
--><!--ᚦ
    «@DeltaHash.T
    -- by which we mean the type paramter that we happen to use for DeltaHash»
--><!--ᚦ
    «@deltaProof we call it a "Balance proof" later--what should we call it (mainly)?»
--><!--ᚦ
    «What is THE expected publicly known value, called a _balancing value_
    and/or where is it defined?»
-->

!!! warning

    Given that we duplicate the roots in the compliance proving records now, do we still need the list of roots in the transaction?<!--
    «@"compliance proving records" do we mean by compliance units?»
    --> <!--ᚦ
    «If in doubt: keep it and/or make a github issue out of this?»
    -->


## Interface

1. `create(Set CMtree.Value, Set Actions) -> Transaction`<!--ᚦ
   «so create is not a transaction function,
   but it was one if we had the inputs as hard coded constants?
   See also the type of `prog` in
   [partial evalutaion](https://en.wikipedia.org/wiki/Partial_evaluation)
   »
-->
2. `compose(Transaction, Transaction) -> Transaction`
3. `verify(Transaction) -> Bool`

## `create`
Given a set of roots and a set of actions, a transaction is formed as follows:

1. `tx.CMTreeRoots = CMTreeRoots`
2. `tx.actions = actions`
3. `tx.transactionDelta = sum(action.Delta() for action in actions)`
4. `tx.deltaProof = DeltaProvingSystem(deltaProvingKey, deltaInstance, deltaWitness)`<!--ᚦ
   «Where do these three parameters come from?
   They are not mentioned above in `## Interface`»
-->

## `compose`

Having two transactions `tx1` and `tx2`, their composition `compose(tx1, tx2)` is defined as a transaction `tx`, where:

1. `tx.CMTreeRoots = Set.union(tx1.CMTreeRoots, tx2.CMTreeRoots)`
2. `tx.actions = Set.union(tx1.actions, tx2.actions)`
3. `tx.deltaProof = DeltaProvingSystem.aggregate(tx1.deltaProof, tx2.deltaProof)`
4. `tx.transactionDelta = tx1.transactionDelta + tx2.transactionDelta`

!!! note "Composing transactions"

    When composing transactions, action sets are simply united without [composing the actions themselves](./action.md#composition). For example, composing a transaction with two actions and another transaction with three actions will result in a transaction with five actions.
    <!--ᚦ«what happens if the union is not disjoint?»-->

## `verify`

A transaction is considered _valid_ if the following statements hold:

Checks that do not require access to global structures:

1. all actions in the transaction are valid, as defined per [action validity rules](./action.md#validity)
1. actions partition the state change induced by the transaction:
  1. there is no resource created more than once across actions
  2. there is no resource consumed more than once across actions
3. `deltaProof` is valid

<!--ᚦ
    «"state change induced by the transaction" just so that we do not forget:
    at some point we may want to say that
    `transaction` is a shorthand for `transaction object`
    @"induced by" could the be "described by"
    (because the transaction object itself is not a doing anything)»
--><!--ᚦ
    «wikilinks preferable /
    we should support [[Page Name#Section Heading|Link Text]] (if we do not yet)»
-->

Checks that require access to global `CMTree` and `NullifierSet`:
<!--ᚦ
    «So, should we mention these as part of the inputs to verify?»
-->

1. each NON-EPHEMERAL??? created resource wasn't created in prior transactions
2. each NON-EPHEMERAL!!! consumed resource wasn't consumed in prior transactions

<!--ᚦ
    «the case of
    "Ephemeral resources do not get checked for existence when being consumed"
    seems clear»
--><!--ᚦ
    «the phrase "in prior transactions" should probably be spelled out
    in terms of CMTree and NullifierSet, respectively»
-->


A transaction is *executable* if it is valid and `transactionDelta` commits to the expected balancing value.
<!--ᚦ
    «what is "the expected balancing value"?
    Where is it defined?
    I also thought that for executability,
    we need (the counterpart of) 0 as trasnactionDelta?
    »
--><!--ᚦ
    «Can we call a transaction object _balanced_ when
    `transactionDelta` commits to the expected balancing value?»
-->

<!--ᚦtags:nits,inconsistent,improvable,reviewed-->

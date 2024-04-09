# Resource logic DAGs

!!! note

    For details about the implementation of `Resources` see [Resource Management](../resource.md#resource-management).

The resource logic DAG provides an abstraction of a _linear resource logic_ with which distributed applications can model finite objects. This logic is based on a concept of a _resource_, which is a unique datum created at a particular point in logical time and possibly consumed later in logical time. Each resource is an instance of a particular _resource logic_, which specifies how (under what conditions) resources of that type can be created and consumed. The resource logic DAG tracks when resources are created and when they are consumed. Resources are only allowed to be consumed after they have been created.  At any point in logical time, the resource logic DAG has a state consisting of all resources which have been created but not consumed.

The resource logic DAG also tracks linear logic violations (duplicate consumptions of the same resource, or "double spends"). Each resource has an ordered list of controller identities, where a valid signature from the last identity in the list is required to consume the resource. At any point in logical time, the latest (right-most) controller of a resource is responsible for ordering possibly conflicting transactions. Resources can be transferred to a new controller (modulo additional validation in the predicates) by appending to the list, or as a special case, they can be transferred to the previous controller (dropping an item from the end of the list). In the case of a double-spend of a resource - namely, a non-total order of two conflicting transactions both signed by the current controller - the conflict is resolved by the controller one element earlier in the list when the resource is eventually transferred back, and in the case of multiple double-spends recursively until the originator (at which point, if they also double-spend, linearity is violated, but as if the originator had just issued more resources, and in any case there is no in-system recovery possible at this point). Controller identities can be defined in particular ways which encode bespoke conflict resolution logic. Recovery from linearity violations does not require any reversal or reordering of transactions, as we keep this explicit "chain of promises" of controllers, so if some controller `I` double-spends, subsequent resources with `I` in the controller list may simply no longer be redeemable back along the original path. By accepting resources with a particular path of controllers, an application or user accepts the double-spend risk of any of the controllers, which can be mitigated by waiting for those controllers to sign over the transaction (which finalises it and guarantees future redemption from their perspective).

## Transaction DAG

!!! todo

     Decide which parts of this subsection should still be moved to Resource Management.

A _transaction_ in a resource logic DAG consists of a balanced set of partial transactions (`ptx`s), which consume a (possibly empty) set of existing resources and create a (possibly empty) set of new resources. Transactions are atomic, in that either the whole transaction is valid (and can be appended to / part of a valid resource logic DAG), or the transaction is not valid and cannot be appended to / included in the resource logic DAG.

!!! todo

     Describe the structural correspondence of `ptx`s to partially applied functions.

!!! note

    For validation criteria of Transactions, see [here](../resource.md#transactions-tx).

A transaction is _consistent_ w.r.t. a physical DAG `D` if and only if:
- All consumed resources were previously created by a transaction in the history, which was itself (recursively) consistent and final

A transaction is _final_ w.r.t. a physical DAG `D` if and only if:
- it is balanced and valid
- it is consistent w.r.t. `D`
- the latest owners of all consumed resources have signed over it in `D`
- all consumed resources have not been consumed by another antecedent transaction in `D` which was itself final

In the case of two _conflicting_ transactions, where the rightmost controller(s) `c` did not totally order them, resolution is defined as:
- the transaction ordered first by the rightmost controller after dropping the last element of the list, or in case of another conflict (by them), drop the last element of the list and repeat. if the end of the list is reached, both transactions are valid (this may violate linearity guarantees), and we rely on some sort of out-of-band fault resolution

Agents, then, have _safe finality_ under the assumption of correct behavior of the earliest controller in the list from whom they have obtained a signature.

## Resource Frontier

For Linear Resources, we can also derive the Resource frontier of the whole graph or subgraph(s), which consists of all resources which have been created but not consumed at that point in logical time.

For Non-Linear Resources, the Frontier contains all Resources ever created.

## Resource Reference

A `Resource Reference` is defined as the Resource Frontier of the Resources inhabiting a specific Resource Type. Typically these will be used for Types with only one inhabitant at each time in history.

More specific references can be defined at higher layers, using entries in static or dynamic `extra_data` fields.

## Delayed execution transactions

Transactions may want to choose their exact input and output resources on the basis of the state just prior to application of the transaction to the state (when it is "executed", or so to speak), in order to, for example, read the most current resource at a particular (known) key and thus avoid conflicts. To facilitate this, transactions in the resource logic DAG can also be modeled as functions which _produce_ transactions, possibly taking into account the latest resource at a particular key. This entails an ordering with respect to the keys read, so the transaction must include all keys which it might read (for which the transaction author does not necessarily know the values and/or wishes ordering to be delegated). The transaction then receives the values of those keys at the logical time of execution and can use them to compute the input and output resources.

!!! todo

     Strict ordering is required here, so if all keys do not have the same identity, we will need to create a joint identity (chimera-chain-on-demand) to try to order w.r.t. all involved resources.

!!! todo

     I think we can/should combine this with executable transaction so in-between states are possible.

```haskell
data DelayedTx
  = DelayedTx {
    keys :: Set Key,
    exec :: Set (Key, Resource) -> Transaction
  }
```

## DAG

```haskell
type Transaction = ResourceLogicTx

type State = Set Resource
```

A resource logic DAG is valid if and only if:
- all transactions are valid by the conditions as above
- all transactions are included in the same order as their data in the physical DAG (i.e. if `a` happens no later than `b` in the physical DAG, `a` happens no later than `b` in the logical DAG)
  - within ordering determined by the physical DAG, creations and consumptions determine ordering within the logical DAG, i.e. a transaction `b` which consumes a resource created by `a` happens after `a`

From a particular resource logic DAG, an observer can calculate a _state_ as a key-value mapping by taking `key(resource)` and `(data resource, value resource)` for all resources created but not yet consumed (by final transactions) in the history of that DAG.

!!! todo

     Examples for data and values.

---

!!! todo

     This section is notes, readers please ignore.

Outstanding topics:
- What exactly is the desired logic of a finality predicate? I think, from the intent layer, it is: "among the transactions which consume my intent and are valid, pick this one". It should not be more general than that because other constraints could have been encoded into the predicates already - finality predicate is only for _ranking_ in information uncertainty, and it is an _ordering_ which should also reference a _logical time_ (w.r.t. some identity). Then the question becoems how ranking functions are _combined_ across intents - we should be able to retain the guarantee that between two transactions with the same intents, where all intent authors prefer the latter, the former is not accepted. Given a set of intents included in a set of transactions, the ranking functions give a partial order to the transactions.  -- then these should _not_ be first-class, rather they are part of the definition of an identity, since ordering/ranking is concerned. So instead we should contemplate ways of encoding this into consensus providers'
- Previously we had this concept of a "virtual resource" for modelling non-linear (infinitely consumable) things. However, since often these were physical-DAG-dependent, I think identity is the right abstraction here instead, maybe it would be good to come up with some motivating examples.
- Spell out how nullifiers and commitments can be used to track linearity efficiently here.

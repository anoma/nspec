# Transaction With Payment

`TransactionWithPayment` is a data structure that allows paying for the desired state transitions.

## Definition

`TransactionWithPayment` contains the following fields:

||Type||
|-|-|-|
|`stateTransitionFunction`|`TransactionFunction`| The desired state update.|
|`paymentTransaction`|`Transaction`|The payment transaction. It is unbalanced, contains consumed resources (gas payment sent) but not created (the receiver is not specified). Includes in a special application data field the hash of the transaction function and the gas limit.|
|`gasLimit`|`Arithmetic`|The maximum amount of gas can be used for execution of the `StateTransition`|

### Execution

When executing a `TransactionFunctionWithPayment`, the executor takes the following steps:

1. Checks that `paymentTransaction` is “simple”. What exactly this means can be executor-specific, but roughly “simple” means “inexpensive to verify”. A basic (very restrictive) check could be that the payment transaction has exactly one consumed resource and nothing else.
2. Decide whether this gas payment is sufficient. This decision can be controller-specific (maybe there are certain assets and certain prices accepted for gas).
3. Alter `paymentTransaction`, adding new resources assigned to the executor (or whoever is supposed to receive the gas payments) as necessary to make the payment transaction balanced.
4. Verify `paymentTransaction`, including in a special application data field the hash of the transaction function and the gas limit.
5. Execute `paymentTransaction` (apply the state changes).
6. Evaluate `stateTransitionFunction`, limited by `gasLimit`.
7. If `stateTransitionFunction` evaluation finishes within `gasLimit` (returning a transaction object), check that the transaction object is valid and balanced, and if so apply it to state (as previously in the RM).
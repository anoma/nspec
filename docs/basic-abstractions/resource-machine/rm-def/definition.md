---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource machine

A **resource machine** is a deterministic stateless machine that creates, composes, and verifies transaction functions.

It has read-only access to the external global state, which includes the content-addressed storage system (which in particular stores resources), global commitment accumulator, and the global nullifier set, and can produce writes to the external local state that will later be applied to the system state.

The resource machine has two layers: the outer layer, the resource machine shell, that creates and processes **transaction functions**, and the inner layer, the resource machine core, that creates and processes **transactions**.

We assume the shell is trivial in this version of the ARM: it only evaluates the transaction function without any verification steps. The result is a transaction that is then passed to the core. The distribution of responsibilities between the shell and the core is expected to change.

To support the shell layer, the resource machine must have the functionality to produce, compose, and evaluate transaction functions. Assuming the shell is trivial in the current version of the specification, the following description of the resource machine functionality describes the functionality of the resource machine core.

A transaction function is defined as `TransactionFunction`: `()` $\rightarrow$ `Transaction`.

See section 8.1 for a description of what data the transaction function can read during execution.

## Post- and pre-ordering execution

*Pre-ordering execution* implies partial evaluation of the transaction function. In practice pre-ordering execution happens before the transactions are ordered by the ordering component external to the ARM.

*Post-ordering execution* implies full evaluation of the transaction function. As the name suggests, post-ordering execution happens after the ordering component external to the ARM completed the ordering of transaction functions.

## ARMs as intent machines

Together with $(CMtree, NFset)$, the Anoma Resource Machine forms an instantiation of the intent machine, where the state $S = (CMtree, NFset)$, a batch $B = Transaction$, and the transaction verification function of the resource machine corresponds to the state transition function of the [intent machine](). To formally satisfy the intent machine's signature, the resource machine's verify function may return the processed transaction along with the new state.



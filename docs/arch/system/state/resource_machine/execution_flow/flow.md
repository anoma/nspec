# Intro

This section describes the resource machine execution flow and how it is used by various actors.

# Resource machine

A **resource machine** is a deterministic stateless machine that creates, composes, and verifies transaction functions.

It has read-only access to the external global state, which includes the content-addressed storage system (which in particular stores resources), global commitment accumulator, and the global nullifier set, and can produce writes to the external local state that will later be applied to the system state.

The resource machine must have the functionality to produce, compose, and evaluate transaction functions and transactions.

Actors working with resource machine include users, solvers, and executor nodes.


### Users
Users are the initiators of the state change. To initiate the state change, users send the information about the desired state change to solvers. Users own the resources to be consumed/created in the transaction, meaning they are the `nullifierKey` holders and they control the transaction authorisation mechanism (resource logics).

Users are not always online and limited in computational power.

Users can create initial actions and transactions that don't require matching, but are assumed to delegate all matching computations to solvers (note that users can take the solver role for themselves as well). To create such transactions, users are expected to be able to do all of the things required to create a transaction, which includes creating all existing data structures, creating all types of proofs, and being able to access the global state.

### Solvers

Solvers are the parties that have the computational power. Solvers are the parties that see intents and try to match them and output a transaction. Users give solvers the data required to create the future transactions, which may include resource objects, `nullifierKey`, signed messages, etc. Given the data, solvers create, compose, and verify transactions. Once the transaction is complete and valid, the transaction function is sent for ordering.

### Executor

Executors are the final nodes that receive transaction functions after ordering and produce a state change. After receiving a transaction function, the executor runs it, outputting a transaction that describes a state update. The executor node validates the resulting transaction, by performing the checks described [here](./../data_structures/transaction.md#verify). In case the transaction is valid, the executor applies the state changes: adds nullifiers to the nullifier set, commitments to the commitment tree, and possibly some other data to the storage.

## Post- and pre-ordering execution

*Pre-ordering execution* implies partial evaluation of the transaction function. In practice pre-ordering execution happens before the transactions are ordered by the ordering component external to the ARM.

*Post-ordering execution* implies full evaluation of the transaction function. As the name suggests, post-ordering execution happens after the ordering component external to the ARM completed the ordering of transaction functions.

# Intro

This section describes the resource machine execution flow and how it is used by various actors. 

# Resource machine

A **resource machine** is a deterministic stateless machine that creates, composes, and verifies transaction functions.

It has read-only access to the external global state, which includes the content-addressed storage system (which in particular stores resources), global commitment accumulator, and the global nullifier set, and can produce writes to the external local state that will later be applied to the system state.

The resource machine has two layers: the outer layer, the resource machine shell, that creates and processes **transaction functions**, and the inner layer, the resource machine core, that creates and processes **transactions**.

We assume the shell is trivial in this version of the ARM: the state change object is travelling over the network in the form of a transaction function, but reaching the ARM, it is evaluated without any verification steps. The result is a transaction that is then passed to the core for processing. The distribution of responsibilities between the shell and the core is expected to change. 

To support the shell layer, the resource machine must have the functionality to produce, compose, and evaluate transaction functions. Assuming the shell is trivial in the current version of the specification, the following description of the resource machine functionality describes the functionality of the resource machine core.

Actors working with resource machine include users, solvers, and executor nodes. 

#### Resource machine functions

A resource machine provides the following functions:

- **Create**: given a set of components required to produce a transaction, the create function produces a transaction data structure according to the [transaction creation rules]().
- **Compose**: taking two transactions $tx_1$ and $tx_2$ as input, produces a new transaction $tx = tx_1 \circ tx_2$ according to the [transaction composition rules]().
- **Verify**: taking a transaction as input, verifies its validity according to the [transaction validity rules](). If the transaction is valid, the resource machine outputs a state update. Otherwise, the output is empty.


# Transaction function

A transaction function is a function that outputs a transaction: `transactionFunction() -> Transaction`.

Transaction functions take no input but can perform I/O operations to read information about global state either by reading data at the specified global storage address or by fetching data by index. The requirements for transaction functions are further described [here]().


### Users
Users are the initiators of the state change. To initiate the state change, users send the information about the desired state change to solvers. Users own the resources to be consumed/created in the transaction, meaning they are the `nullifierKey` holders and they control the transaction authorisation mechanism (resource logics).

Users are not always online and limited in power.

Users can create initial actions and transactions that don't require matching, but are assumed to delegate all matching computations to solvers (note that users can take the solver role for themselves as well). To create such transactions, users are expected to be able to do all of the things required to create a transaction, which includes creating all existing data structures, creating all types of proofs, and being able to access the global state.

### Solvers

Solvers are the parties that have the computational power. Solvers are the parties that see intents and try to match them and output a transaction. Users give solvers the data required to create the future transactions, which may include resource plaintexts, `nullifierKey`, signed messages, etc. Given the data, solvers create, compose, and verify transactions. Once the transaction is complete and valid, the transaction function is sent for ordering.

### Executor

Executors are the final nodes that receive transaction functions after ordering and produce a state change. After receiving a transaction function, the executor runs it, outputting a transaction that describes a state update. The executor node validates the resulting transaction, by performing the checks described [here](./../data_structures/transaction.md#verify). In case the transaction is valid, the executor applies the state changes: adds nullifiers to the nullifier set, commitments to the commitment tree, and possibly some other data to the storage.
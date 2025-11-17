# Proof aggregation
An aggregation proof attests to the validity of all compliance and logic proofs of an RM transaction. With aggregation, the [raw RM proofs](../proving/index.md) (except the delta proof) do not need to be stored in the transaction structure. Reducing thereby verification time and transaction size.

## Aggregation inputs
#### Witness
* the list of [compliance proofs](../../resource_machine/data_structures/compliance_unit/compliance_proof.juvix.md) of the RM transaction,
* the list of [logic proofs](../../resource_machine/data_structures/action/resource_logic_proof.juvix.md) of the RM transaction.

#### Instance
* the [compliance verifying key](../../resource_machine/data_structures/compliance_unit/compliance_unit.juvix.md#compliance-unit),
* The list of [logic verifying keys](../../resource_machine/data_structures/action/index.juvix.md###logicVerifyingInputs) of the RM transaction,
* The list of [compliance instances](../../resource_machine/data_structures/compliance_unit/compliance_proof.juvix.md####instance) of the RM transaction,
* The list of [logic instances](../../resource_machine/data_structures/action/resource_logic_proof.juvix.md####instance) of the RM transaction.

!!! note
    Passing the raw proofs as witnesses means they are not needed to verify the aggregation proof. This is what allows to remove them from the RM transaction.

!!! note
    The verifier must be aware of what has been verified by the prover during aggregation. That is why we include the raw verifying keys and raw instances. However, they do not need to appear explicitly. A _binding_ (and possibly short) commitment suffices.
## Aggregation constraints
An aggregation circuit must check the following:
1. Verify each compliance proof against its corresponding compliance instance using the compliance verifying key.
2. Verify each logic proof against its corresponding logic instance using the corresponding logic verifying key.
3. Possibly, other aggregation-specific constraints (which depends on the aggregation strategy implemented).

## Aggregation strategies
**Batch aggregation**. All compliance and logic proofs of an RM transaction are verified in a single run of the aggregation program. The batch aggregation instance is exactly the list of compliance and logic verifying keys and instances present in the RM transaction.

**Sequential aggregation**. The aggregation is an incrementally verified computation (IVC). At each step, a single raw proof (either compliance or logic proof) is verified against a passed instance and verifying key. To keep track of the instances and keys verified at previous steps, they are accumulated in a chained hash. Correct accumulation is also enforced. The sequential aggregation instance is the hash of all compliance and logic verifying keys and instances of the RM transaction.

!!! note
    The sequential aggregation is an example of proof-carrying data (PCD) computation. PCD-based aggregation can be distributed across mutually untrusted nodes, and proofs to be aggregated arbitrarily grouped and arranged in different transcripts. Parallel proving at the ARM level would be possible with a tree-like transcript.

## Verifying transactions
Aggregation is an optional feature. Transactions may or may not come with an aggregation proof.

* If there is an aggregation proof, verify it using the aggregation verifying key. The aggregation instance must be derived appropriately from the raw instances and raw verifying keys.
* Otherwise, the raw proofs must be present. Verify them all against the raw instances using the raw verifying keys.
* In either case, verify the [delta proof](../../resource_machine/data_structures/transaction/delta_proof.juvix.md).

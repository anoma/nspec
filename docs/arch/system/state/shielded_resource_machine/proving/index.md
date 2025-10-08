# Proving systems

The table below describes what proving system we use to instantiate which proof type.

| RM Statement | Representation    | Proof type    |
| ------------ | ----------------- | ------------- |
| Compliance   | [Risc0 circuit]     | STARK/Groth16 |
| Logic        | [Risc0 circuit]     | STARK/Groth16 |
| Delta        | [Binding signature] | ECDSA         |

We differentiate between two kinds of proofs depending on how closely they interact with sensitive data:

1. **Raw RM proofs** - the proofs produced directly by RM for each transaction. Include compliance proofs, logic proofs, and delta proofs.
2. **Aggregated proof** - combines the raw RM proofs into a fixed number of proofs per transaction. Currently, aggregation results in two proofs per transaction: aggregated SNARK proofs and a delta proof (untouched).

| Proof stage       | Scope                                                             |
| ----------------- | ----------------------------------------------------------------- |
| Raw proofs        | Action (logic), compliance unit (compliance), transaction (delta) |
| Aggregated proofs | Single transaction                                                |

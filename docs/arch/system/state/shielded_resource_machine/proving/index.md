# Proving


| RM Statement | Representation    | Proof type    |
| ------------ | ----------------- | ------------- |
| Compliance   | Risc0 circuit     | STARK/Groth16 |
| Logic        | Risc0 circuit     | STARK/Groth16 |
| Delta        | Binding signature | ECDSA         |

We differentiate between three "stages" of proofs depending on how closely they interact with sensitive data:

- **Raw RM proofs** - the proofs produced directly by RM for each transaction. Include compliance proofs, logic proofs, and delta proofs.
- **Aggregated proof** - combines the raw RM proofs into a fixed number of proofs per transaction. Currently, aggregation results in two proofs per transaction: aggregated SNARK proofs and a delta proof.
- **Execution proof** - a proof over multiple transactions that verifies the global execution checks in a verifiable manner. The execution proof doesn't have to be zk.

| Proof stage       | Scope                                                             |
| ----------------- | ----------------------------------------------------------------- |
| Raw proofs        | Action (logic), compliance unit (compliance), transaction (delta) |
| Aggregated proofs | Single transaction                                                |
| Execution proof   | Multiple transactions                                             |

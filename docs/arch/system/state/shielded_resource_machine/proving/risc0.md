# RISC Zero proving system

Compliance and logic constraints are represented as RISC Zero programs. [RISC Zero](https://risczero.com/) is a zkVM based on [STARK proofs](https://eprint.iacr.org/2018/046). Each program in RISC Zero (called session) is split into segments of equal length (determined by the cycle count) and proven separately (segment proofs) which are then aggregated (succinct proof). That implies that:

1. the bigger the program is, the more segment proofs are required and the longer it takes to prove the whole session
2. memory requirements are bound (segment memory upper bound)
3. the final proof size is fixed
4. verification time is fixed

## Groth16 recursive proofs for faster on-chain verification
RISC Zero zkVM also supports creating [Groth16](http://eprint.iacr.org/2016/260.pdf) proofs for faster verification. Groth16 proofs have minimal proof size (3 field elements) but require trusted setup for each circuit. Therefore Groth16 isn't suitable for creating proofs of various programs but allows efficient verification of a fixed program. RISC Zero zkVM provides a groth16 circuit that verifies recursively an aggregated segment proof.

Raw RM proofs (compliance and logic) are STARK proofs. For efficient on-chain verification, they can be wrapped in Groth16, either via [proof aggregation](./proof_aggregation.md) or directly.

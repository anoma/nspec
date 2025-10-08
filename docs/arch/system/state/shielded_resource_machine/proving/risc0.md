# Risc0

Both compliance and logic proofs are represented as [RISC Zero circuits](https://risczero.com/).

#### RISC Zero overview
RISC Zero is a zkVM based on [STARK proofs](https://starkware.co/blog/scaling-blockchains-with-zero-knowledge-proofs/#starks). Each program in RISC Zero (called session) is split into segments of equal length (determined by the cycle count) and proven separately (segment proofs) which are then aggregated (succinct proof). That implies that:
- the bigger the program is, the more segment proofs are required and the longer it takes to prove the whole session
- memory requirements are bound (segment memory upper bound)
- the final proof size is fixed
- verification time is fixed

##### Groth16 recursive proofs for faster on-chain verification
RISC Zero zkVM also supports creating [Groth16](http://eprint.iacr.org/2016/260.pdf) proofs for faster verification. Groth16 proofs have minimal proof size (3 field elements) but require trusted setup for each circuit. Therefore Groth16 isn't suitable for creating proofs of various programs but allows efficient verification of a fixed program. RISC Zero zkVM provides a groth16 circuit that verifies recursively an aggregated segment proof.

Raw RM proofs (compliance and logic) are STARK proofs. For efficient on-chain verification, they are wrapped in Groth16, via proof aggregation or directly.

# Delta Proving System

`DeltaProvingSystem`:

- `Prove (PS.ProvingKey, PS.Instance, PS.Witness) -> PS.Proof`
- `Verify (PS.VerifyingKey, PS.Instance, PS.Proof) -> Bool`
- `Aggregate(PS.Proof, PS.Proof) -> PS.Proof` - allows to aggregate two proofs s.t. 
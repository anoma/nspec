### Resource Structure

| Component|Description| Formula|
|-|-|-|
| `logicRef` | Logic reference is a verifying key of the logic circuit. Risc0 verifying keys are SHA256 hashes.||
| `labelRef` | Fixed size binding commitment to the label. | $SHA256(label)$|
| `valueRef` | Fixed size binding commitment to the value. | $SHA256(value)$|
| `quantity` |`u128` |
| `isEphemeral`| `Bool` |
| `nonce`| Guarantees the uniqueness of the commitment and nullifier. Computed from the nullifier of the resource consumed in the same compliance unit.| $nonce_{created} = nf_{consumed}$|
| `nullifierKeyCommitment` |More details can be found [here]() | $cnk = SHA256(nk)$|
| `randSeed` | Generated randomly when the resource is created ||
| `kind` | | $kind = SHA256(logicRef \|\| labelRef)$|
| `psi`| A parameter used to compute the resource nullifier| $psi = SHA256("RISC0\_ExpandSeed" \|\| 0 \|\| randSeed \|\| nonce)$|
| Resource commitment randomness `rcm` | Ensures hiding properties of the resource commitment| $rcm = SHA256("RISC0\_ExpandSeed" \|\| 1 \|\| randSeed \|\| nonce)$|
| Resource commitment `cm` | Unique identifier of a created resource | $cm = SHA256(logicRef, labelRef, valueRef,$ $quantity, isEphemeral, nonce$$, nullifierKeyCommitment, rcm)$|
| Resource nullifier `nf`| Unique identifier of a consumed resource| $nf = SHA256(nk, nonce, psi, cm)$|
| `tag`| `cm` for created resources, `nf` for consumed resources ||

## Ephemeral resources

Ephemeral resources are different from the persistent ones in that we don't verify the Merkle path for their existence. Therefore, ephemeral resources can be consumed even if they were not created.

In every other aspect they are treated the same: the commitment is added to the commitment accumulator, the nullifier is added to the nullifier set.

Ephemeral resources of 0 value can be used to include additional constraints in the transaction. Ephemeral resources of non-zero value can be used to carry intents. Ephemeral resources are also used as padding resources when needed. They can be used for other purposes intended by the application.

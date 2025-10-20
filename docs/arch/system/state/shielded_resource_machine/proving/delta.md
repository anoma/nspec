# Delta Proving System

Delta proving system is instantiated with a binding signature. The design of it is based on Zcash binding signature [(Zcash Specification, section 4.13)](https://zips.z.cash/protocol/protocol.pdf), but we extend it to support multiple resource kinds. In binding signature design, the correctness of the balance is proven by the ability to generate the correct signing and verifying keys, the signed message itself plays a secondary role.

## Binding signature

### Computing delta in compliance units

Each compliance unit takes one input and one output resource, the compliance unit delta is computed as: `complianceDelta = inputResource.delta() - outputResource.delta()`. Resource delta is computed as `r.delta() = PedersenCommit(r.quantity, r.kind(), rcv) = r.quantity * r.kind() + rcv * blindBase`
where:

1. `*` is a scalar multiplication EC operation
2. `r.quantity` and `rcv` are scalars
3. `r.kind()` and `blindBase` are EC points
4. `rcv` is random, `blindBase` is fixed

Computing compliance delta from resource deltas is equivalent to computing compliance delta from resource object components directly (i.e., skipping the individual resource delta computation). In practice, we do not compute individual resource deltas. Instead, we compute compliance delta as:  `complianceDelta = inputResource.quantity * inputResource.kind() - outputResource.quantity * outputResource.kind() + rcv * blindBase`

### The mechanism (single kind)

1. Binding signature **signing key** is computed by adding commitment randomness `rcv` from all compliance units in the transaction: $bsk = \sum{rcv}$. Note that `rcv` are secret values.
- **Verifying key** is computed by adding compliance unit deltas together: $bvk=\sum{\delta_{compliance}}$. Note that $\delta_{compliance}$ are public values - anyone can compute binding signature verifying key.
2. For correctly computed `bvk` and `bsk` , `bvk = bsk * blindBase` since individual balances add to 0, which proves that:

  1. the signer knows `rcv` used to compute compliance deltas
  2. the transaction balances to 0 - otherwise, `bvk = bsk * blindBase` wouldn’t be true and the signature wouldn’t verify

##### Extending to multiple kinds

Because of how elliptic curves work ([kind distinctness](https://specs.anoma.net/latest/arch/system/state/resource_machine/primitive_interfaces/fixed_size_type/delta_hash.html?h=kind+distin#delta-hash) holds), having multiple kinds in the same binding signature is equivalent to having multiple binding signatures per each kind. Note that it is all possible because we expect everything balance to 0.

#### Instantiation

| Parameter        | Instantiation                                 |
| ---------------- | --------------------------------------------- |
| Signature scheme | ECDSA                                         |
| Elliptic curve   | k256                                          |
| Hash function    | Keccak256                                     |
| Signed message   | Tags of resources included in the transaction |
| Prove()          | ECDSA.sign(pk, keccak256(message))            |
| Verify()         | ECDSA.verify(vk, proof)                       |

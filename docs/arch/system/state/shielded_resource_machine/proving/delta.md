# Delta Proving System

Delta proof allows verifying that the total transaction delta is equal to `expectedBalance` without seeing individual deltas of resources in the transaction. [^1]

[^1]: Note that currently we only support `expectedBalance = 0`

Delta proving system is instantiated with a binding signature. The design of it is based on Zcash binding signature [(Zcash Specification, ssection 4.13)](https://zips.z.cash/protocol/protocol.pdf), but we extend it to supporting multiple resource kinds. In binding signature design, the correctness of the balance is proven by the ability to generate the correct signing and verifying keys, the signed message itself plays a secondary role.
#### Binding signature

##### Computing delta in compliance units
Each compliance unit takes one input and one output resource, the compliance unit delta is computed as: `complianceDelta = inputResource.delta() - outputResource.delta()`. Resource delta is computed as `r.delta() = PedersenCommit(r.quantity, r.kind(), rcv) = r.quantity * r.kind() + rcv * blindBase`
where:

- `*` is a scalar multiplication EC operation
- `r.quantity` and `rcv` are scalars
- `r.kind()` and `blindBase` are EC points
- `rcv` is random, `blindBase` is fixed

Computing compliance delta from resource deltas is equivalent to computing compliance delta from resource object components directly (i.e., skipping the individual resource delta computation). In practice, we do not compute individual resource deltas. Instead, we compute it as:  `complianceDelta = inputResource.quantity * inputResource.kind() - outputResource.quantity * outputResource.kind() + rcv * blindBase`

##### The mechanism

Let’s assume that we only have resources of the same kind for now.

- Binding signature **signing key** is computed by adding commitment randomness `rcv` from all compliance units in the transaction: bsk=∑rcv. Note that `rcv` are secret values.
- **Verifying key** is computed by adding compliance unit deltas together bvk=∑cu.delta(). Note that `cu.delta()` are public values - anyone can compute binding signature verifying key.
- For correctly computed `bvk` and `bsk`, `bvk = bsk * blindBase` since individual balances add to 0, which proves that:
    - the signer knows `rcv` used to compute compliance deltas
    - the transaction balances to 0 - otherwise, `bvk = bsk * blindBase` wouldn’t be true and the signature wouldn’t verify

##### Extending to multiple kinds

Because of how elliptic curves work ([kind distinctness](https://specs.anoma.net/latest/arch/system/state/resource_machine/primitive_interfaces/fixed_size_type/delta_hash.html?h=kind+distin#delta-hash) holds), having multiple kinds in the same binding signature is equivalent to having multiple binding signatures per each kind. Note that it is all possible because we expect everything balance to 0.

#### Instantiation

| Parameter        | Instantiation                                 |
| ---------------- | --------------------------------------------- |
| Signature scheme | ECDSA                                         |
| Elliptic curve   | k256                                          |
| Hash function    | Keccak256                                     |
| Signed message   | Tags of resources included in the transaction |
| Prove()          | ECDSA.sign(pk, keccak256(message))            |
| Verify()         | ECDSA.verify(vk, proof)                       |

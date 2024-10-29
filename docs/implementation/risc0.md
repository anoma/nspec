---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# RISC0

## Primitive choices

### Risc0 VM

- Frontend Language: Rust
- Instruction Set Architecture (ISA): RISC-V

The Risc0 Resource Machine (RM) inherits some security properties from the underlying Risc0 Virtual Machine (VM) upon which is built. We highlight these below:

#### Proof system

- **Arithmetization**: Plonkish (UltraPlonk in particular). The arithmetization consists of customised gates, high-degree polynomial relations, many witness wires, and lookup arguments.
- **Polynomial evaluation and commitment (PCS)**: FRI (Fast Reed-Solomon Interactive Proof of Proximity).
- **Prime field $\mathbb{F}$**: The computation is defined over the BabyBear field (modulus $15 \cdot 2^27 + 1$) and a degree-four extension is used during the algebraic holographic proving. Each BabyBear element stores one byte of the data. In other words, a 32-bit integer uses four BabyBear elements.
- **Memory checking**: Each access to the main memory always incurs only a constant overhead. Pages are authenticated using Merkle Trees.
- **STARK-to-SNARK**: Proof generation results in STARK proofs that can be further compressed—without revealing information and in a trustless way—into very succinct SNARK proofs through Groth16.

#### Security analysis
| Prover               | Cryptographic Assumptions                                         | Bits of Security | Quantum Safe? |
|----------------------|-------------------------------------------------------------------|------------------|---------------|
| RISC-V Prover        | - Random Oracle Model<br>- Toy Problem Conjecture                 | 97               | Yes           |
| Recursion Prover     | - Random Oracle Model<br>- Toy Problem Conjecture                 | 99               | Yes           |
| STARK-to-SNARK Prover| - Security of elliptic curve pairing over BN254<br>- Knowledge of Exponent assumption<br>- Integrity of Groth16 Trusted Setup Ceremony | 99+              | No            |

On-chain verifier contracts target 97 bits of security.

The best known attack vector against our STARK to SNARK Prover is to attack the underlying elliptic curve pairing used with BN254. This primitive has been heavily battle-tested: it's part of the core cryptography on Zcash and it's included as a precompile on Ethereum (see EIP-197).

### Risc0 RM

#### Resource primary fields

Since the Risc0 proving system is based on hashes and not on elliptic curves, the cryptographic primitive used for compressing, hiding and binding data in Merkle tree structures such as the resource commitment tree, or others such as the nullifier set in the Risc0 RM is sha256. Furthermore, whenever we encounter a PRF in the ARM specs, we can substitute it for sha256 in the Risc0 RM.

If homomorphism is required, we operate on the secp256k1 curve. We use lowercase for fields (Babybear) and uppercase for points in curve (secp256k1). For instance, $[x] \cdot G$ denotes scalar multiplication of a curve point $G$.


| Field | Computation | Type/size | Description |
|----------|---------|-----------|-------------|
| l        | sha256(verifying_key(RL)) | Digest ($256$ bits) | Application's RL verifying key. Used to identify the application the resource belongs to. As the verifying key itself is large, resources only store a commitment to it.
| label    |    user defined     |     unsigned integer ($256$ bits)     | Contains the application data that affects fungibility of the resource. Along with \( l \), it is used to derive the resource's kind. |
| q        | user defined |  unsigned integer ($256$ bits)| The quantity of fungible value. |
| v        |  user defined       |    unsigned integer ($256$ bits)       | Resource value is a commitment to the resource's extra data that doesn't affect the resource's fungibility. |
| eph      | user defined  | bool (1 bit)   | Ephemeral resource flag. It indicates whether the resource's commitment Merkle path should be checked when consuming the resource. |
| nonce    | n $\overset{\$}{\leftarrow} \mathbb{F}$; sha256(n) | Digest ($256$ bits) | Guarantees the uniqueness of the later derived computable fields. |
| npk      | sha256(nsk) | Digest ($256$ bits) | Commitment to the nullifier key \( nk \) that will be used to derive the resource's nullifier. |
| rseed    | $\overset{\$}{\leftarrow} u256$ | unsigned integer ($256$ bits)  | A random commitment trapdoor. |

#### Resource computable fields

Computable fields are fields derived by applying some computation on the resource primary fields listed above.

| Field | Computation | Type/size | Description |
|----------|---------|-----------|-------------|
| K | secp256k1::hash_to_point(l, label) | secp256k1 point | Resource kind |
| cm | sha256(l, label, q, v, eph, npk, nonce, npk, rseed) | Digest ($256$ bits) | Resource commitment. It allows to prove the existence of the resource without revealing the resource plaintext. |
| nf | sha256(nk, nonce, cm) | Digest ($256$ bits) | Resource nullifier. Revealing the resource's nullifier invalidates the resource. All nullifiers are stored in a global append-only nullifier set. |
| D | $[q_1] \cdot K_1 - [q_2] \cdot K_2 + [rcd] \cdot R$ | secp256k1 point | Resource delta used to ensure balance across the resources ($r_1$, $r_2$) in a transaction. $rcd$ is some random value in $0 ... 2^{256}-1$ and $R$ is a secp256k1 point of unknown discrete log. |


### Cryptographic algorithms

#### Verifiable encryption

We want the encryption to be verifiable to make sure the receiver of the resources can decrypt them.

Since the Risc0 proving system uses a small field, bit-wise operations' efficiency is acceptable. Thus we use the [AES encryption algorithm](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).




## Encoding choices

### Resource

```rust
pub struct Resource {
    // a succinct representation of the predicate associated with the resource
    pub l: Digest,
    // specifies the fungibility domain for the resource
    pub label: [u8; 32],
    // number representing the quantity of the resource
    pub quantity: [u8; 32],
    // the fungible data of the resource
    pub value: [u8; 32],
    // flag that reflects the resource ephemerality
    pub eph: bool,
    // guarantees the uniqueness of the resource computable components
    pub nonce: Digest,
    // nullifier public key
    pub npk: Npk,
    // randomness seed used to derive whatever randomness needed
    pub rseed: [u8; 32],
}
```

where `Npk` is just a wrapper over `Digest` (which is in turn a wrapper over an unsigned integer of 256 bits) used for type safety.

### Compliance circuit

```rust
pub struct Compliance<const COMMITMENT_TREE_DEPTH: usize> {
    /// The input resource
    pub input_resource: Resource,
    /// The output resource
    pub output_resource: Resource,
    /// The path from the output commitment to the root in the resource commitment tree
    pub merkle_path: [(Digest, bool); COMMITMENT_TREE_DEPTH],
    /// Random scalar for delta commitment
    pub rcv: ScalarWrapper,
    /// Nullifier secret key
    pub nsk: Nsk,
}
```

where `ScalarWrapper` is just a wrapper over an unsigned integer of 256 bits, and `Nsk` is also a wrapper over `Digest`. `Nsk` and `Npk` are related as follows:

```rust
pub struct Nsk(Digest);
pub struct Npk(Digest);

impl Nsk {
    pub fn new(nsk: Digest) -> Nsk {
        Nsk(nsk)
    }
    /// Compute the corresponding nullifier public key
    pub fn public_key(&self) -> Npk {
        let bytes: [u8; DIGEST_BYTES] = *self.0.as_ref();
        Npk(*Impl::hash_bytes(&bytes))
    }
}
```

#### Commitment tree
- Data Structure
- Operations & Complexity
- Hash function

#### Nullifier set
- Data structure
- Operations & Complexity
- Hash function

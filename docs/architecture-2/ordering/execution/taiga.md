---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Taiga

Taiga is a concrete instantiation of the [[Resource Machine|Anoma Resource Machine]] used to compute and verify state transition proposals. Taiga defines what a valid transaction is and provides the means to produce and verify transactions.

A valid **transaction** is defined by two criteria:
- applications the state of which is being affected by the proposed state transition authorize the change
- the proposed state transition doesn't violate the Taiga rules

Actors and agents use Taiga to produce and verify the proofs required to form transactions. The executor function uses Taiga to verify the transactions before applying them to the state.

## Resource model

Being an instance of the Anoma Resource Machine, Taiga is designed in the resource model, where resources represent atomic units of the state. Taiga supports shielded state transitions with the help of zero-knowledge proofs, commitment schemes, signatures, and other privacy-preserving techniques. Resources are distributed and stored in an encrypted form. Taiga uses proof recursion to provide function privacy for custom logics.

Taiga was heavily inspired by [Zcash Orchard](https://github.com/zcash/zips/blob/main/protocol/protocol.pdf) and [ZEXE](https://eprint.iacr.org/2018/962).

## Functions provided by Taiga

- **create a transaction:** users create initial transactions to announce what they offer and request, including constraints. These transactions are sent to the intent gossip network to be matched with other transactions. Solvers create transactions to match the intents of the users.
- **verify a transaction:** each transaction contains proofs attesting to its correctness. When a solver receives transactions from the intent gossip network, they must verify the proofs.
- **compose transactions:** solvers combine transactions to build a balanced transaction that satisfies the intents of the involved parties.

The following sections describe the protocol for shielded state transitions.

!!! note

    Instantiations and some of the exact formulas are unstable

!!! note

    To learn more about Taiga as a standalone component, check [the Taiga repository](https://github.com/anoma/taiga)

## 1. Proving systems

The table below contains the description of how resource machine proof types are instantiated by Taiga.

|RM proof|Type|Instantiation|
|-|-|-|
|Delta proof|Binding signature|RedDSA + Pasta curves|
|Compliance proof|zk-SNARK|Halo2 + IPA FCS + Pasta curves|
|Resource logic proof|zk-SNARK|Halo2 + IPA FCS + Pasta curves|

A zero-knowledge proving system is used to produce zero-knowledge proofs for the compliance circuit and resource logic circuits. The compliance circuit is fixed, resource logic circuits are custom and require at least two-layer recursion to achieve function privacy. Currently, Taiga uses Halo2 with IPA FCS and [Pasta curves](https://github.com/zcash/pasta) to create proofs for these circuits.

### 1.1 zk-SNARK circuits

A circuit $C$ is represented as polynomials over the chosen curve's **scalar field**, following [plonk-ish arithmetization](https://zcash.github.io/halo2/concepts/arithmetization.html). Proof elements are generated over the curve's **base field**.

### 1.2 Elliptic curves

||Name|Scalar field| Base field|Purpose|Instantiation|
|-|-|-|-|-|-|
|$E_I$|Inner curve|$\mathbb{F}_q$|$\mathbb{F}_p$|ECC gadget| [Pallas](https://github.com/zcash/pasta#pallasvesta-supporting-evidence)
|$E_M$|Main curve|$\mathbb{F}_p$|$\mathbb{F}_q$|compliance and RL circuits| [Vesta](https://github.com/zcash/pasta#pallasvesta-supporting-evidence)|
|$E_O$|Outer curve|$\mathbb{F}_q$|$\mathbb{F}_p$|Accumulation circuit| Pallas|

### 1.3 Proving system interfaces

||Interface|Description|
|-|-|-|
|__Generate Verifying key__|`keygen_vk(C) ⟶ vk`|`C` is turned into a *verifying key* — a succint representation of the circuit that the verifier uses to verify a proof|
|__Generate Proving key__|`keygen_pk(C, vk) ⟶ pk`|Generate a proving key from a verifying key and an instance of the circuit|
|__Prove__|`P(pk, x, w) ⟶ π`|Prove that a circuit is satisfied|
|__Verify__|`V(vk, x, π) ⟶ 0/1`|Verify the proof|

## 2. Resources

A *resource* is an immutable particle of an application state. The state is updated by consuming and creating resources.

### 2.1 Resource plaintext

The table below describes the components of a resource, also referred as a resource plaintext.

|Variable|Formula|Type/size|Description|
|-|-|-|-|
|$l$|$VKCommit(vk_{logic})$||Contains the application's RL verifying key. Used to identify the application the resource belongs to. As the verifying key itself is large, resources only store a commitment to it|
|$label$|||Contains the application data that affects fungibility of the resource. Along with $l$, it is used to derive resource's kind|
|$q$||${0..2^{64} - 1}$|The quantity of fungible value|
|$v$|||Resource value is a commitment to the resource's extra data that doesn't affect the resource's fungibility|
|$eph$||bool|Ephemeral resource flag. It indicates whether the resource's commitment Merkle path should be checked when consuming the resource.|
|$nonce$|$nonce$|$\mathbb{F}_p$|An old nullifier from the same Compliance description|
|$npk$|$cm_{nk}$||Commitment to the nullifier key $nk$ that will be used to derive the resource's nullifier. $npk = NKCommit(nk)$|
|$rseed$||$\mathbb{F}_p$|A random commitment trapdoor|

!!! note

    The value size cannot be bigger or close to the curve's scalar field size (to avoid overflowing) but besides that there are no strict reasons for choosing 64. We can use more resources to express a value that doesn't fit in one resource (splitting the value into limbs). Having bigger value size requires fewer resources to express such a value and is more efficient. For example, a value size of 128 bits would require two times less resources to express a maximum value

### 2.2 Computable fields

#### 2.2.1 Resource kind

Each resource has a kind that refers to the application the resource belongs to. It is derived from the resource's logic and label as follows:

$K = PRF^{kind}(l, label)$

#### 2.2.2 $\psi$

This an intermediate computed parameter used in the computation of resource commitment and resource nullifier.
$\psi = PRF^{\psi}(0, rseed, nonce)$

!!! note

    unstable

#### 2.2.3 $rcm$

This parameter is used as randomness when computing the resource commitment.

$rcm = PRF^{rcm}(1, rseed, nonce)$

!!! quote

    unstable

#### 2.2.4 Resource commitment

Resource commitment allows to prove the existence of the resource without revealing the resource plaintext. For a resource $r$, the resource commitment is computed as follows: $cm = \mathrm{ResourceCommit}(r.l, r.label, r.v, r.npk, r.nonce, r.\psi, r.eph, r.q., r.rcm)$.

Resource commitments are stored in a global append-only commitment tree $CMtree$, which contains commitments to all of the resources that were ever created. $CMtree$ is a cryptographic accumulator implemented as a Merkle tree. To prove the resource's existence, a path to the resource's commitment leaf is provided as a witness (private input).

#### 2.2.5 Nullifier

Revealing the resource's nullifier invalidates the resource. All nullifiers are stored in a global append-only nullifier set $NFset$. Given the nullifier key $nk$ and a resource $r$, the nullifier $nf$ is computed as follows: $nf = DeriveNullifier_{nk}(r) = PRF_{nf}(r.nk, r.nonce, r.\psi, r.cm)$

##### 2.2.5.1 Nullifier key $nk$

Each created resource plaintext contains a nullifier public key $npk$ that commits to some nullifier key $nk$. This nullifier key have to be used to compute the resource's nullifier. The knowledge of the resource's nullifier key is necessary (but not sufficient) to create the resource's nullifier and invalidate the resource.

$nk \mathop{\longleftarrow}\limits^{R} \mathbb{F}_p$

### 2.5 Verifiable encryption

Encryption is used for in-band distribution of resources. Encrypted resources are stored on the blockchain, the receiver can scan the blockhcain trying to decrypt the transactions to find the resources that were sent to them.

We want the encryption to be verifiable to make sure the receiver of the resources can decrypt them. In other systems like Zcash the sender and the creator of the resource are the same actor, and it doesn't make sense for the sender to send a corrupted message to the receiver (essentially burning the resource), but in Taiga the resources are often created and sent by different parties.

For verifiable encryption, we use the combination of DH key exchange for key derivation and symmetric encryption.

$sk = DH(pub_{recv}, priv_{send})$

$ce = Encrypt(resource, sk)$

Not all of the resource fields require to be encrypted (e.g. the resource commitment), and the encrypted fields may vary depending on the application. To make sure it is flexible enough, the encryption check is performed in RL circuits (as opposed to verifying the encryption in the compliance circuit).

### 2.6 Ephemeral resources

Ephemeral resources are resources for which the existence (i.e., Merkle path to its commitment in the $CMtree$) is not checked when the resource is being consumed. Unlike some other systems (e.g., Zcash), resource's ephemerality isn't defined by its quantity (i.e., resources of quantity 0 are not necessarily ephemeral), instead, it is explicitly defined by the ephemerality flag $eph$. Non-zero value ephemeral resources can be handy for carrying additional constraints (e.g. intents) and for balancing transactions.

## 3. Circuits

### 3.1 The Compliance Circuit

The compliance circuit `ComplianceCircuit(x; w)` checks that a transaction satisfies the Taiga rules. The Compliance circuit performs checks over $1$ input and $1$ output resource, which sometimes referred as a compliance pair. A transaction containing $n$ input and $n$ output resources requires $n$ Compliance proofs. If the number of input and output resources isn't equal, ephemeral notes can be used to make them equal. The circuit is arithmetized over $\mathbb{F}_p$.

#### Inputs

Public inputs ($x$):
1. $rt$ - $CMtree$ root
2. $cm$ - output resource commitment
3. $cm_{l}^{out}$ - commitment to the output resource's logic,
2. $nf$ - input resource nullifier
5. $cm_{l}^{in}$ - commitment to the input resource's logic
6. $\Delta$ - compliance pair delta

Private inputs ($w$):
1. $path$ - $CMtree$ path from $rt$ to $cm$
2. $r^{in}$ - input resource plaintext
3. $(l^{in}, rcm^{in}_{l})$ - $cm_{l}^{in}$ opening
4. $r^{out}$ - output resource plaintext
5. $(l^{out}, rcm^{out}_{l})$ - $cm_{l}^{out}$ opening

!!! note

     opening of a parameter contains every component of the parameter

#### Checks

- For the input resource:
    - If `eph = true`, check that the resource is a valid resource in $rt$: there is a path in Merkle tree with root $rt$ to a resource commitment $cm$ that opens to $r$
      - $path$ leads from $rt$ to $cm$
      - $cm$ commits to $r^{in}$
    - Nullifier integrity: $nf = DeriveNullifier_{nk}(r^{in})$.
    - Resource logic integrity: $cm_{l}^{in} = RLCommit(l^{in}, rcm^{in}_{l})$
    - Kind integrity: $K = PRF^{kind}(l^{in}, label^{in})$
- For the output resource:
    - Commitment integrity: $cm = ResourceCommit(r^{out}, rseed^{out})$
    - Resource logic integrity: $cm_{l}^{out} = RLCommit(l^{out}, rcm^{out}_{l})$
    - Kind integrity: $K = PRF^{kind}(l^{out}, label^{out})$
- Delta integrity: $delta = DeltaCommit(q_{in}, q_{out}, K_{in}, K_{out}, rcd)$

!!! note

     unlike [MASP](https://github.com/anoma/masp), the value base in Taiga is not used to compute resource's commitment and the compliance circuit doesn't take $kind$ as private input but computes it from the resource fields, and it is checked for both input and output resources.

### 3.2 Resource Logic (RL) circuits

Resource logic is a circuit containing the application logic. Resource logics take $m$ input and $n$ output resources, are represented as Halo2 circuits `RL(x; w) ⟶ 0/1` and arithmetized over $\mathbb{F}_p$.

#### Inputs

Public inputs ($x$):
- $nf_1, …, nf_m$ - input resource nullifiers
- $cm_1, …, cm_n$ - output resource commitments
- $ce_1, …, ce_n$ - encrypted output resources
- custom public inputs

Private inputs ($w$):
- $r^{in}_1, …, r^{in}_m$ - input resources openings
- $r^{out}_1, …, r^{out}_n$ - output resources openings
- $tag$ that identifies the resource for which the resource logic is being checked
- custom private inputs

Each resource logic has a fixed number of public inputs and unlimited amount of private inputs. Currently, the allowed number of public inputs is limited to $25$.

#### Checks

As the resource plaintexts are private inputs, to make sure that resources that the circuit received indeed the ones that correspond to the public parameters, every RL circuit must check:

1. Input resource nullifier integrity: for each $i ∈ {1, …, m}, nf_i = DeriveNullifier_{nk}(nonce, \psi, cm)$
2. Output resource commitment integrity: for each $i ∈ {1, …, n}, cm_i = ResourceCommit(r)$
3. Encrypted output resource integrity: for each $i ∈ {1, …, n}, ce_i = Encrypt(r, pub\_recv)$

!!! quote

    **Note:** encryption can be customized per application. Some applications might encrypt more fields, others - less. The size of the encrypted resource does leak some information.

All other constraints enforced by RL circuits are custom.

#### Finding the owned resources

A resource logic takes all resources from the current $tx$ as input which requires a mechanism to determine which resource is the resource being currently checked. Currently, to determine that, Taiga passes the resource commitment (for output resources) or the nullifier (for input resources) of the owned resource as a tag. The RL identifies the resource that is being checked by its tag.

#### RL commitment

In the presence of a RL proof for a certain resource, RL commitment is used to make sure the right RL is checked for the resource. It makes sure that $vk_{logic}$ the resource refers to and $vk_{logic}$ used to validate the RL proof are the same.

RL commitment has a nested structure:
- $cm_{l} = RLCommit(l, rcm_{l})$
- $l = VKCommit(vk_{logic})$

The check is done in two steps:
1. The Compliance circuit checks that the RL commitment $cm_{l}$ is derived with the $l$ the resource refers to:
$cm_{l} = RLCommit(l, rcm_{l})$
2. The verifier circuit checks that the RL commitment is computed using the $vk_{logic}$ that is used to validate the RL proof:
$cm_{l} = RLCommit(VKCommit(vk_{logic}), rcm_{l}) (l = VKCommit(vk_{logic}))$

!!! quote

    $VKCommit$ is not implemented yet and currently $l = Blake2b(vk_{logic})$

As the outer commitment $RLCommit$ is verified in both the compliance and verifier circuit which are arithmetized over different fields, the outer commitment instantiation should be efficient over both fields.

As the inner commitment $VKCommit$ is only opened in the verifier circuit, it only needs to be efficient over the $E_O$ scalar field.

## 4. Circuit Accumulation

TBD: Halo2 accumulation

#### 5. Delta (balance commitment) & delta proof

Delta parameter is used to ensure balance across the resources in a transaction. In Taiga, delta is computed directly for compliance pairs and transactions (not for individual resources).

For a compliance pair of one input and one output resources, delta is computed as follows:

$\Delta_{compl} = DeltaCommit(q^{in}, K^{in}, q^{out}, K^{out}, rcd) = \lbrack q^{in} \rbrack K^{in} - \lbrack q^{out}\rbrack K^{out} + \lbrack rcd\rbrack R$

|Variable|Type/size|Description|
|-|-|-|
|$q^{in}$|${0..2^{64} - 1}$|input resource's quantity|
|$q^{out}$|${0..2^{64} - 1}$|output resource's quantity|
|$K^{in}$|$E_O$ point|input resource's kind|
|$K^{out}$|$E_O$ point|output resource's kind|
|$R$|$E_O$ point|randomness base, fixed|
|$rcd$|${0..2^{255} - 1}$|delta randomness|
|$\Delta_{compl}$|$E_O$ point|compliance pair delta|

For an initial transaction containing $n$ compliance pairs, delta is computed as follows:

$\Delta_{tx} =  \sum{\Delta_{compl_i}}$

For a transaction $tx$ composed from transactions $tx_1$ and $tx_2$, $\Delta_{tx} = \Delta_{tx_1} + \Delta_{tx_2}$.

### 5.1 Binding signature (delta proof)

Binding signature is used to prove that the transaction is correctly balanced. Delta parameters produced in each transaction used to compose the current transaction being checked are accumulated and checked against the commitment to the expected net value change. Currently, Taiga uses the same binding signature mechanism as Zcash Orchard.

#### Taiga balance vs Application balance

Taiga transaction is balanced if for each resource kind: $\sum_i{v_i^{in}} - \sum_j{v_j^{out}} = v^{balance}$, where $v^{balance}$ is the balancing value. Applications have their own definitions of balance that might differ from the Taiga definition. For example, some applications might allow to create more output value from less input value, which makes the total value change $v^{balance}$ non-zero. In case when Taiga's balancing value is assumed to be zero, the application-specific balance is different from the Taiga balance and the application needs to make sure the transaction is balanced in the Taiga sense by adding some non-zero value ephemeral resources to the transaction.

## 6. Instantiations

|Function|Instantiation|Domain/Range|Description|
|-|-|-|-|
|$PRF^{nf}$|Poseidon|$\mathbb{F_p^4} \rightarrow \mathbb F_p$|$PRF^{nf}_{nk}(nonce, \psi, cm) = Poseidon(nk, nonce, \psi, cm)$|
|$PRF^{kind}$|Poseidon|$\mathbb{F_p^2} \rightarrow \mathbb{E_I} $|$PRF^{kind} = \mathtt{hash\_to\_curve}(Poseidon(l, label))$
|$PRF^{rcm}$|Poseidon|$ \mathbb{F_p^3} \rightarrow \mathbb F_p$|Used to derive resource commitment randomness|
|$PRF^{\psi}$|Poseidon|$\mathbb{F_p^3} \rightarrow \mathbb F_p$|Used to derive $\psi$|
|||||
|$NKCommit$|Poseidon|$\mathbb{F_p^2} \rightarrow \mathbb F_p$|$NKCommit(nk, k) = Poseidon(nk,k)$; used to compute $npk$, user-derived key $k$ is currently not used|
|$ResourceCommit$|Poseidon|$\mathbb{F_p^9} \rightarrow \mathbb F_p$|
|$DeltaCommit$|Pedersen commitment with variable value base|$\mathbb{F_q^2} \times \mathbb{E_I^2} \times \mathbb{F_q} \rightarrow \mathbb{E_I}$|
|$RLCommit$|Blake2s|-|Efficient over both $\mathbb F_p$ and $\mathbb F_q$
|$VKCommit$|-|-|Efficient over the $E_O$ scalar field; not implemented yet (it is checked in the verifier circuit that is not implemented)|
|||||
|$Encrypt$|DH + Poseidon|$\mathbb F_p \rightarrow \mathbb F_p$| $Encrypt(r, pub_{recv}, priv_{send}) = Poseidon(r, DH(pub_{recv}, priv_{send}))$
|Binding signature|RedDSA||

## 7. Transaction

#### Components

Each Taiga $tx$ contains:
- $n$ compliance proof records (one compliance proof covers one input and one output resource), each containing:
    - $\pi_{compl}$ - compliance proof
    - $vk_{compl}$ - compliance circuit verifying key
    - $(rt, cm, cm^{out}_{l}, nf, cm^{in}_{l}, \Delta)$ - compliance proof public input
- resource logic's proving record for every resource created/consumed in the $tx$:
    - $\pi_{l}$ - resource logic proof
    - $vk_{logic}$ - resource logic verifying key
    - public inputs, including commitments and encryptions of the created resources and nullifiers of the consumed resources
- binding signature
- transaction delta $\Delta_{tx}$
- extra data $extra$
- preference function $\Phi$

#### Validity of a transaction

A transaction is valid if:
1. For each compliance proof:
    - if `eph = true`, `rt` must be a valid $CMtree$ root.
    - $Verify(\pi_{compl}, vk_{compl}, CompliancePublicInput) = True$
2. For each resource logic proof:
    - $Verify(\pi_{l}, vk_{logic}, LogicPublicInput) = True$
    - Public input consistency: resource logic public input $nf$ and $cm$ are the same as in the compliance public input
3. Binding signature is valid for $\Delta_{tx}$

!!! note

     Currently, each resource requires a separate RL proof, even if they belong to the same application. Eventually the RL might be called just once per $tx$, meaning that if the $tx$ has 2 or more resources belonging to the same application, the total amount of non-ephemeral proofs is reduced.

!!! note

     It is possible that a resource logic requires checks of other logics in order to be satisfied. In that case, the total amount of logic proofs verified could be more than $2n$, but we can count such check as a single check.

### Taiga state

Taiga doesn't store a state, but Taiga produces state changes (that will be executed elsewhere), that include:
- For each created resource $r$, $CMtree.WRITE(r.cm)$,
- For each consumed resource $r$, $NFset.WRITE(r.nf)$,

## 8. Communication between the shielded and transparent pools

State transitions that do not preserve privacy are called *transparent*. Assuming that the system allows both transparent and shielded state transitions, we say that all of the valid resources created as a result of shielded state transitions form a *shielded pool* and the valid resources created as a result of transparent state transitions form a *transparent pool*. The action of moving data from transparent to shielded pool is called *shielding*, the opposite is called *unshielding*. Shielding (or unshielding) is done by consuming resources in one pool and creating the corresponding resources in the other. *Balancing value* $v^{balance}$ indicates the data move between the pools:
- $v^{balance} = 0$ if the current transaction doesn't move data between pools
- $v^{balance} < 0$ refers to the value moved from the transparent to the shielded pool
- $v^{balance} > 0$ refers to the value moved from the shielded to the transparent pool

!!! note

     That the balancing value corresponds to the data flow between pools only for transactions processed in post-ordering execution. Transactions before ordering might not necessarily correctly represent the data flow between the pools.

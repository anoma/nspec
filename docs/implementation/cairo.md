---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Cairo

Note: The structs and APIs in Juvix are used for writing circuits, including compliance circuit and resource logic circuits. Meanwhile, the Elixir structs and APIs are utilized outside of the circuit to build the Resource Machine.

## Primitive choices

### Baisc finite field and curve
The basic data type in Cairo is [felt252](https://docs.starknet.io/architecture-and-concepts/cryptography/p-value/), which is a large prime number, currently equal to P = 2^{251} + 17 * 2^{192}+1.

We're using the native [STARK curve](https://docs.starknet.io/architecture-and-concepts/cryptography/stark-curve/) based on the felt252 in Cairo RM.

### Hash Funtion
The built-in [Poseidon hash](https://docs.starknet.io/architecture-and-concepts/cryptography/hash-functions/#poseidon_hash) and [Pedersen hash](https://docs.starknet.io/architecture-and-concepts/cryptography/hash-functions/#pedersen_hash) of Cairo VM are used to construct the Cairo RM.

#### Poseidon Hash
The Poseidon hash is widely used to construct other primitives like Merkle trees, commitments, nullifiers, etc.

#### Poseidon Hash in Juvix

```juvix
poseidonHash1 (x : Field) : Field

poseidonHash2 (x y : Field) : Field

poseidonHashList (list : List Field) : Field
```

#### Poseidon Hash in Elixir
```Elixir
@spec poseidon_single(list(byte())) :: list(byte())

@spec poseidon(list(byte()), list(byte())) :: list(byte())

@spec poseidon_many(list(list(byte()))) :: list(byte())
```

#### Pedersen Hash
The Pedersen hash is used to calculate the `kind` of resource in the compliance circuit by passing `resource.logic` and `resource.label`.

```juvix
pedersenHashToCurve (x y : Field) : Ec.Point
```

### Commitment

```Elixir
@spec commitment(ShieldedResource.t()) :: binary()
@doc "A commitment to the given resource."
def commitment(resource = %ShieldedResource{}) do
psi =
    Cairo.poseidon_many([
    Constants.prf_expand_personalization_felt(),
    Constants.felt_zero(),
    resource.rseed,
    resource.nonce
    ])

rcm =
    Cairo.poseidon_many([
    Constants.prf_expand_personalization_felt(),
    Constants.felt_one(),
    resource.rseed,
    resource.nonce
    ])

Cairo.poseidon_many([
    resource.logic,
    resource.label,
    resource.data,
    resource.npk,
    resource.nonce,
    psi,
    resource.quantity,
    resource.eph,
    rcm
])
end
```

### Nullifier

```Elixir
@spec nullifier(ShieldedResource.t()) :: binary()
@doc """
The nullifier of the given resource.
"""
def nullifier(resource = %ShieldedResource{}) do
psi =
    Cairo.poseidon_many([
    Constants.prf_expand_personalization_felt(),
    Constants.felt_zero(),
    resource.rseed,
    resource.nonce
    ])

Cairo.poseidon_many([
    resource.npk,
    resource.nonce,
    psi,
    commitment(resource)
])
```

#### Nullifier public key(Nullifier key commitment)

```Elixir
@spec get_npk(binary()) :: binary()
@doc """
Generate the nullifier public key from the nulliffier (private)key.
"""
def get_npk(nk) do
Cairo.poseidon(
    nk,
    Constants.felt_zero()
)
|> :binary.list_to_bin()
end
```

### Binding signature for the delta proof

```Elixir
@spec cairo_binding_sig_sign(list(list(byte())), list(list(byte()))) ::
        list(byte())
def cairo_binding_sig_sign(_private_key_segments, _messages)

@spec cairo_binding_sig_verify(
        list(list(byte())),
        list(list(byte())),
        list(byte())
    ) :: boolean()
def cairo_binding_sig_verify(_pub_key_segments, _messages, _signature),
```

### Verifiable Encryption

```Elixir
@spec encrypt(list(list(byte())), list(byte()), list(byte()), list(byte())) ::
        list(byte())
def encrypt(messages, pk, sk, nonce)

@spec decrypt(list(list(byte())), list(byte())) :: list(byte())
def decrypt(cihper, sk)
```

The `encrypt` in Juvix circuit can be found [here](https://github.com/anoma/aarm-cairo/blob/base/native/cairo_vm/encryption.juvix).

## Encoding choices

The basic `felt252` in Anoma RM(Elixir) is a `binary()` type with a length of 32 bytes or 256 bits.

### ShieldedResource

#### ShieldedResource in Anoma RM(Elixir)
```Elixir
typedstruct enforce: true do
    # resource logic
    field(:logic, binary(), default: <<0::256>>)
    # fungibility label
    field(:label, binary(), default: <<0::256>>)
    # quantity
    field(:quantity, binary(), default: <<0::256>>)
    # arbitrary data
    field(:data, binary(), default: <<0::256>>)
    # ephemerality flag
    field(:eph, bool(), default: false)
    # resource nonce
    field(:nonce, binary(), default: <<0::256>>)
    # nullifier public key
    field(:npk, binary(), default: <<0::256>>)
    # random seed
    field(:rseed, binary(), default: <<0::256>>)
end
```

#### ShieldedResource in circuits(Juvix)
```juvix
type Resource :=
  mkResource {
    logic : Field;
    label : Field;
    quantity : Field;
    data : Field;
    eph : Bool;
    nonce : Field;
    npk : Field;
    rseed : Field
  };
```

### ProofRecord
The `ProofRecord` does not explicitly contain a verifying key since it is already embedded in the `proof` by the STARK proving system. We provide an additional API to obtain the hash of the verifying key for out-of-circuit verification purposes.

```Elixir
typedstruct enforce: true do
    field(:proof, binary(), default: <<>>)
    field(:public_inputs, binary(), default: <<>>)
end

@spec get_cairo_program_hash(ProofRecord.t()) :: binary()
def get_cairo_program_hash(proof_record)
```

### ComplianceInput(compliance private inputs)
The private and public inputs in zkvms are generally substituted with program inputs and outputs to enhance the intuitiveness of vm design. We derive the concepts in Cairo RM. The Cairo(STARK) proving system requires JSON format inputs. We also offer an API to generate the JSON string from `ComplianceInput`.

```Elixir
typedstruct enforce: true do
    # Input resource
    field(:input_resource, ShieldedResource.t())
    # Input resource merkle path
    field(:merkel_proof, CommitmentTree.Proof.t())
    # Nullifier key of the input resource
    field(:input_nf_key, binary(), default: <<0::256>>)
    # Ephemeral root
    field(:eph_root, binary(), default: <<0::256>>)
    # Output resource
    field(:output_resource, ShieldedResource.t())
    # Random value in delta proof(binding signature)
    field(:rcv, binary(), default: <<0::256>>)
end

@spec to_json_string(ComplianceInput.t()) :: binary()
@doc """
Generate the compliance input json
"""
def to_json_string(input) do

```

### ComplianceOutput(compliance public inputs)
```Elixir
typedstruct enforce: true do
    # Input Resource nullifier
    field(:nullifier, binary(), default: <<0::256>>)
    # Output Resource commitment
    field(:output_cm, binary(), default: <<0::256>>)
    # Resource commitment Merkle tree root
    field(:root, binary(), default: <<0::256>>)
    # Resource delta
    field(:delta_x, binary(), default: <<0::256>>)
    field(:delta_y, binary(), default: <<0::256>>)
    # Input Resource logic
    field(:input_logic, binary(), default: <<0::256>>)
    # Output Resource logic
    field(:output_logic, binary(), default: <<0::256>>)
end
```

### ResourceLogicOutput(resource logic public inputs)

```Elixir
typedstruct enforce: true do
    # Self resource identity: nullifier of input resource or commitment of output resource
    field(:self_resource_id, binary())
    # The merkle root of resources in ptx
    field(:root, binary())
    # Ciphertext
    field(:cipher, list(binary()))
    # Custom outputs
    field(:others, list(binary()))
end
```

### ShieldedAction
The roots, commitments, and nullifiers are all integral components of the `ProofRecord` object, thus they are not explicitly listed in the `ShieldedAction`. Nevertheless, we do provide APIs to retrieve them instead.

```Elixir
typedstruct enforce: true do
    field(:logic_proofs, list(ProofRecord.t()), default: [])
    field(:compliance_proofs, list(ProofRecord.t()), default: [])
end

@spec verify(ShieldedAction.t()) :: boolean()
@doc """
verify all the compliance and resource logic proofs, and other correspondence checks
"""
def verify(action)
```

### ShieldedTransaction
```Elixir
typedstruct enforce: true do
    field(:roots, list(binary()), default: [])
    field(:commitments, list(binary()), default: [])
    field(:nullifiers, list(binary()), default: [])
    field(:actions, list(ShieldedAction.t()), default: [])

    # When the tx is not finalized(balanced), the delta is the collection of private keys
    # to generate the delta proof(binding signature).
    # The delta should be the binding signature once the tx is finalized.
    field(:delta, binary(), default: <<>>)
end

@spec verify(ShieldedTransaction.t()) :: boolean()
@doc """
verify all the actions and delta proof
"""
def verify(transaction)

@spec resource_existence_check(ShieldedTransaction.t(), any()) :: boolean()
@doc "check the existence of merkle roots"
def resource_existence_check(transaction, storage)

@spec resource_existence_check(ShieldedTransaction.t(), any()) :: boolean()
@doc "check the non-existence of nullifiers"
def nullifier_check(transaction, storage)
```

## Other decisions

### Nullifiers and commitments correspondence check between compliances and resource logics

To support varying numbers of resources in the Action and prevent information leakage in shielded RM, we are constructing a compact Merkle tree within the resource logic to verify nullifier and commitment correspondence. The resource merkle path in the logic circuit proves the existence of resources in the current execution context, while the out-of-circuit root check occurs in `Action.verify()`.

```Elixir
typedstruct enforce: true do
    # The resource merkle tree
    field(:tree, CommitmentTree.t())
    # The merkle root of resources in ptx
    field(:root, binary())
    # The tree leaves: help find the target index
    field(:leaves, list(binary()))
end

@spec construct(CommitmentTree.Spec.t(), list(binary())) :: ResourceTree.t()
@doc """
construct the tree from leaves
"""
def construct(spec, leaves)

@spec prove(ResourceTree.t(), binary()) :: list() | nil
@doc """
generate the merkle path for the leaf
"""
def prove(tree, leaf)
```

## Some juvix circuits in practice
[Compliance circuit](https://github.com/anoma/aarm-cairo/blob/base/native/cairo_vm/compliance.juvix)

[A trivial resource logic circuit](https://github.com/anoma/aarm-cairo/blob/base/native/cairo_vm/trivial_resource_logic.juvix)

[Encryption circuit](https://github.com/anoma/aarm-cairo/blob/base/native/cairo_vm/encryption.juvix)(should be an recommended function using in resource logics)
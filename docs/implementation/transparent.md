---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Transparent

Transparent Resource Machine Implementation Details per v0.25.0

## Primitive choices

### Commitment Hash
We commit a resource compiled to Nock by jamming a resource and pre-pending
the binary with "CM_":

#### Hoon Primitive

```hoon
++  commit  ::  commit to a resource
  |=  =resource
  ^-  commitment
  (~(cat block 3) 'CM_' (jam resource))
```

#### Elixir Primitive

```elixir
@spec commitment(Resource.t()) :: binary()
def commitment(resource = %Resource{}) do
    binary_resource = resource |> to_noun() |> Nock.Jam.jam()
    "CM_" <> binary_resource
end
```

### Nullifier Hash
We nullify a resource compiled to Nock by jamming a resource and
pre-pending the binary with "NF_":

#### Hoon Primitive

```hoon
++  nullify  ::  nullify a resource
  |=  =resource
  ^-  nullifier
  (~(cat block 3) 'NF_' (jam resource))
```

#### Elixir Primitive

```elixir
@spec nullifier(Resource.t()) :: binary()
def nullifier(resource = %Resource{}) do
    binary_resource = resource |> to_noun() |> Nock.Jam.jam()
    "NF_" <> binary_resource
end
```



### Merkle Tree Hash
Our hash used for the Merkle Tree instantiation is `sha 256`:

#### Hoon Primitive
Not instantiated.

#### Elixir Primitive

```elixir
@spec sha256(iodata()) :: binary()
def sha256(a) do
  :crypto.hash(:sha256, a)
end
```

## Encoding choices

### Public and Private Inputs

#### Hoon Encoding

```hoon
+$  public-inputs
  $:
    commitments=(list @)
    nullifiers=(list @)
    self-tag=@
    other-public=*
  ==
+$  private-inputs
  $:
    committed-resources=(list resource)
    nullified-resources=(list resource)
    other-private=*
  ==
```

#### Elixir Encoding

Not instantiated.

### Resource Logic

#### Hoon Encoding
```hoon
+$  resource-logic
  $~  =>(~ |=(* &))
  $-([public-inputs private-inputs] ?)
```

#### Elixir Encoding

Not instantiated.

### Resource

#### Hoon Encoding
```hoon
+$  resource
  $~  :*
    label=*@t
    logic=*resource-logic
    ephemeral=|
    quantity=`@u`1
    data=*[@u @]
    nullifier-key=*@I
    nonce=*@I
    rseed=%fake
  ==
  $:
    label=@t
    logic=resource-logic
    ephemeral=?
    quantity=@u
    data=[len=@u val=@]
    nullifier-key=@I
    nonce=@I
    rseed=%fake
  ==
```

#### Elixir Encoding
```elixir
typedstruct enforce: true do
    field(:label, binary(), default: "")
    field(:logic, Noun.t(), default: [[1 | 0], 0 | 0])
    field(:ephemeral, bool(), default: false)
    field(:quantity, non_neg_integer(), default: 1)
    field(:data, binary(), default: <<>>)
    field(:nullifier_key, ed25519_public(), default: <<0::256>>)
    field(:nonce, <<_::256>>, default: <<0::256>>)
    field(:rseed, <<>>, default: <<>>)
end
```

### Complicance Proof

#### Hoon Encoding
```hoon
+$  compliance-proof  %compliance
```

#### Elixir Encoding

Not instantiated.

### Logic Proof

#### Hoon Encoding
```hoon
+$  logic-proof
  [resource=resource inputs=[public-inputs private-inputs]]
```

#### Elixir Encoding
```elixir
typedstruct enforce: true do
    field(:resource, Resource.t())
    field(:commitments, MapSet.t(Resource.commitment()),
      default: MapSet.new()
    )
    field(:nullifiers, MapSet.t(Resource.nullifier()), default: MapSet.new())
    field(
      :self_tag,
      {:committed, Resource.commitment()}
      | {:nullified, Resource.commitment()}
    )
    field(:other_public, Noun.t(), default: <<>>)
    field(:committed_plaintexts, MapSet.t(Resource.t()),
      default: MapSet.new()
    )
    field(:nullified_plaintexts, MapSet.t(Resource.t()),
      default: MapSet.new()
    )
    field(:other_private, Noun.t(), default: <<>>)
end
```

### Proof

#### Hoon Encoding
```hoon
+$  proof  ?(compliance-proof logic-proof)
```

#### Elixir Encoding

Not instantiated.

### Action

#### Hoon Encoding
```hoon
+$  action
  $~  :*
    commitments=~
    nullifiers=~
    proofs=~
    app-data=**
  ==
  $:
    commitments=(list @)
    nullifiers=(list @)
    proofs=(list proof)
    app-data=*
  ==
```

#### Elixir Encoding
```elixir
typedstruct enforce: true do
    field(:commitments, MapSet.t(binary()), default: MapSet.new())
    field(:nullifiers, MapSet.t(binary()), default: MapSet.new())
    field(:proofs, MapSet.t(LogicProof.t()), default: MapSet.new())
    field(:app_data, binary(), default: <<>>)
end
```

### Delta

#### Hoon Encoding
```hoon
+$  delta-element
  [k=resource-kind v=@s]
+$  delta  (list delta-element)
```

#### Elixir Encoding
```elixir
@type Delta.t() :: %{binary() => integer()}
```

### Transaction

#### Hoon Encoding
```hoon
+$  transaction
  $~  :*
    roots=~
    actions=~
    delta=*delta
    delta-proof=%delta
  ==
  $:
    roots=(list @)
    actions=(list action)
    delta=delta
    delta-proof=%delta
  ==
```

#### Elixir Encoding
```elixir
typedstruct enforce: true do
    field(:roots, MapSet.t(binary()), default: MapSet.new())
    field(:actions, MapSet.t(Action.t()), default: MapSet.new())
    field(:delta, Delta.t(), default: %{})
    # useless field for shielded only.
    field(:delta_proof, <<>>, default: <<>>)
end
```

## Other decisions

### Compliance Verification

```elixir
@spec verify_tx_action_compliance(t()) :: true | {:error, String.t()}
  def verify_tx_action_compliance(%Transaction{actions: actions}) do
    failed =
      actions
      |> Enum.map(&Action.verify_correspondence/1)
      |> Enum.reject(&(&1 == true))

    Enum.empty?(failed) or
      {:error, Enum.join(Enum.map(failed, &elem(&1, 1)), "\n")}
end
```

with `verify_correspondence` defined as:

```elixir
@spec verify_correspondence(t()) :: true | {:error, String.t()}
  def verify_correspondence(action = %Action{}) do
    # Bail out early, if there are more committed and nullified
    # resources than there are actual resource proofs
    if MapSet.size(action.proofs) <
         MapSet.size(action.commitments) + MapSet.size(action.nullifiers) do
      {:error,
       "there are more commitments and nullifiers than actual logic proofs\n" <>
         "#{inspect(action, pretty: true)}"}
    else
      # TODO Should I check that LogicProof.commitments =
      # Action.commitments, as well as the nullifiers? Or can I assume
      # that they are the same context. I could technically make it
      # lie if I constructed it to lie, no?
      failed_proofs =
        action.proofs
        |> Enum.map(fn proof = %LogicProof{} ->
          cond do
            not LogicProof.verify_resource_corresponds_to_tag(proof) ->
              "Logic Proof failed, the resource's commitment\nullifier:\n" <>
                "#{inspect(proof.resource, pretty: true)}\n" <>
                "does not match the commitment/nullifier: #{inspect(proof.self_tag)}"

            not verify_resource_is_accounted_for?(action, proof) ->
              "The resource:\n" <>
                "#{inspect(proof.resource, pretty: true)}\n" <>
                "Is not found in the Action's commitment/nullifier set"

            not verify_action_resources_correspond_to_proofs?(action, proof) ->
              "Either the action's commitments:\n" <>
                "#{inspect(action.commitments, pretty: true)}" <>
                "does not match the proof's commitments:" <>
                "#{inspect(proof.commitments, pretty: true)}" <>
                "or the action's nullifiers:" <>
                "#{inspect(action.nullifiers, pretty: true)}" <>
                "does not match the proof's nullifiers:" <>
                "#{inspect(proof.nullifiers, pretty: true)}"

            true ->
              true
          end
        end)
        |> Enum.reject(&(&1 == true))

      Enum.empty?(failed_proofs) ||
        {:error,
         "The following correspondence proofs failed:\n" <>
           Enum.join(failed_proofs, "\n")}
    end
end
```



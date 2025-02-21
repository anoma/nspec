---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.resource;
    import prelude open;
    import arch.system.types.nullifierkey open;
    import arch.system.types.delta open;
    import arch.system.types.kind open;
    import arch.system.state.resource_machine.prelude open;
    ```

# Resource

A **resource** is of type `Resource`.

## `Resource`

```juvix
type Resource := mkResource {
  logicRef : LogicHash;
  labelRef : LabelHash;
  valueRef : ValueHash;
  quantity : Nat;
  isEphemeral : Bool;
  nonce : Nonce;
  nullifierKey : NullifierKey;
  randSeed : Nat;
};
```

??? quote "Arguments"

    `logicRef`
    : [[Hash]] of the predicate associated with the resource (resource logic).

    `labelRef`
    : [[Hash]] of the resource label. Resource label specifies the fungibility
    domain for the resource. Resources within the same fungibility domain are
    seen as equivalent kinds of different quantities. Resources from different
    fungibility domains are seen and treated as non-equivalent kinds. This
    distinction comes into play in the balance check described later

    `valueRef`
    : [[Hash]] of the resource value. Resource value is the fungible data
    associated with the resource. It contains extra information but does not
    affect the resource's fungibility

    `quantity`
    : is a number representing the quantity of the resource

    `isEphemeral`
    : is a flag that reflects the resource's ephemerality. Ephemeral resources
    do not get checked for existence when being consumed

    `nonce`
    : guarantees the uniqueness of the resource computable components

    `nullifierKeyCommitment`
    : is a nullifier key commitment. Corresponds to the nullifier key $nk$ used to
    derive the resource nullifier (nullifiers are further described [[Nullifier|here]])

    `randSeed`
    : randomness seed used to derive whatever randomness needed


??? quote "Auxiliary Juvix code"

    ```juvix
    deriving
    instance
    ResourceEq : Eq Resource;
    ```

    ```juvix
    deriving
    instance
    ResourceOrd : Ord Resource;
    ```

## Purpose

A resource represents a uniquely identifiable asset in the system. Resources can
be created, consumed, and transformed according to predefined logic rules.

## Properties

Resources have the following key properties:

- Uniqueness: Each resource instance is uniquely identified by its components
- Fungibility: Resources sharing the same label are considered fungible
- Nullification: Resources can be consumed only once using their [[Nullifier|nullifier key]]
- Ephemerality: Ephemeral resources bypass existence checks when consumed

# Kind

The function `kind` computes the kind of a resource by extracting its label and logic fields.

```juvix
kind (r : Resource) : KindHash :=
  kindHash (Resource.labelRef r) (Resource.logicRef r);
```

## Delta for Resource

Below is the *HasDelta* instance for a `Resource`. It calls `deltaHash` with the
resource’s `kind`, `quantity`, and some `extraInput`.

```juvix
axiom extraInput : ExtraInput;

axiom deltaHash :
  KindHash -> Nat -> ExtraInput -> DeltaHash;

instance
hasDeltaResourceI : HasDelta Resource :=
  mkHasDelta@{
    delta := \{r :=
      deltaHash (kind r) (Resource.quantity r) extraInput
    }
  };
```

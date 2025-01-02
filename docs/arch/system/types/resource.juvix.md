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
    import arch.node.types.crypto open;
    import arch.system.types.nullifierkey open;
    ```

# Resource

A **resource** is of type `Resource`.

## `Resource`

??? quote "Auxiliary Juvix code: Type synonyms"

    For the time being, the following type synonyms are used:

    ### `LogicHash`

    ```juvix
    syntax alias LogicHash := Digest;
    ```

    ### `LabelHash`

    ```juvix
    syntax alias LabelHash := Digest;
    ```

    ### `ValueHash`

    ```juvix
    syntax alias ValueHash := Digest;
    ```

    ### `Nonce`

    ```juvix
    syntax alias Nonce := Nat;
    ```

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

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
    ```

# Resource

A **resource** is a composite structure `Resource` that contains the following components:

## `Resource`

```juvix
type Resource := mkResource {
  -- logicRef : LogicHash;
  -- labelRef : LabelHash;
  valueRef : Digest;
  -- quantity : Quantity;
  isEphemeral : Bool;
  -- nonce : Nonce;
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
    the resource nullifier (nullifiers are further described [[Nullifier|here]])

    `randSeed`
    : randomness seed used to derive whatever randomness needed

To distinguish between the resource data structure consisting of the resource
components and a resource as a unit of state identified by just one (or some) of
the resource computed fields, we sometimes refer to the former as a *resource
object*. Data which is referenced by the resource object - such as the preimage
of `valueRef` - we refer to as *resource-linked data*.


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

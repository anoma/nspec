---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.primitive_interfaces.map;
```

# Map

Map is a structure that contains pairs (key: value), where key is of type `K` and value is of type `V`.

## Interface

1. `new() -> Map`
2. `add(Map, K, V) -> Map`
3. `size(Map) -> Nat`
4. `get(Map, K) -> V`
5. `keys(Map) -> OrderedSet K`


# Used in
1. Action: `applicationData`
2. Action: `proofs`

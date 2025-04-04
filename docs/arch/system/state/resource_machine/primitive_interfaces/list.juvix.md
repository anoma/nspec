---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.primitive_interfaces.ordered_set;
```

# List

1. `new() -> List` - creates an empty list
2. `size(Set) -> Nat` - returns the number of elements in the list
3. `elem(List, Nat) -> T` - returns an element from the list at the given position
4. `append(List, T) -> List` - appends an element to the list
5. `delete(List, Nat) -> List` - removes an element at the given position from the list
6. `contains(List, T) -> Bool` - checks if an element is in the list

## Used in
1. Action (commitments, nullifiers)
2. Compliance unit
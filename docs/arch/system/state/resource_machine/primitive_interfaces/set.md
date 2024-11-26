# Set primitive interface

A set is an unordered data structure that contains only distinct elements.

## The interface

For a set parametrised over the element type `T`:

1. `New() -> Set` - creates an empty set.
2. `New(List) -> Set` - creates a set from the given list of elements. If the list contains duplicating elements, ignores them.
3. `Size(Set) -> Nat` - returns the number of elements in the set.
4. `Insert(Set, T) -> Set` - adds an element of type `T` to the set.
5. `Union(Set, Set) -> Set` - computes the union of two sets.
6. `Intersection(Set, Set) -> Set` - computes the intersection of two sets.
7. `Difference(Set, Set) -> Set` - computes the difference of two sets. Note that this operation is not commutative.
8. `DisjointUnion(Set, Set) -> Set` - computes the union of two sets. If the sets intersect, returns an error.
9. `Contains(Set, T) -> Bool` - checks if an element is in the set.

## Used in
1. Action (commitments, nullifiers)
2. Transaction (roots, actions)
3. Nullifier set
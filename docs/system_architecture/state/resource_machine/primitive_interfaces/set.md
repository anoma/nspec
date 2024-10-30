# Set primitive interface

A set is an unordered data structure that contains only distinct elements.

## The interface

For a set parametrised over the element type `T`:

- `New() -> Set` - creates an empty set.
- `New(List) -> Set` - creates a set from the given list of elements. If the list contains duplicating elements, ignores them.
- `Size(Set) -> Nat` - returns the number of elements in the set.
- `Insert(Set, T) -> Set` - adds an element of type `T` to the set.
- `Union(Set, Set) -> Set` - computes the union of two sets.
- `Intersection(Set, Set) -> Set` - computes the intersection of two sets.
- `Difference(Set, Set) -> Set` - computes the difference of two sets. Note that this operation is not commutative.
- `DisjointUnion(Set, Set) -> Set` - computes the union of two sets. If the sets intersect, returns an error.
- `Contains(Set, T) -> Bool` - checks if an element is in the set.

## Used in
- Action (cms, nfs, $\Pi$)
- Transaction (rts, actions)
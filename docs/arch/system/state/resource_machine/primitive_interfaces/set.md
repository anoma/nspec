# Set primitive interface

A set is an unordered data structure that contains only distinct elements.

<!--ᚦ«Are sets always finite? (they are below)»-->
<!--ᚦ«Could it be a [hash set](https://stackoverflow.com/questions/4558754/define-what-is-a-hashset)?»-->

## The interface

For a set parametrised over the element type `T`:
<!--ᚦ«So it is a set of terms of type $\mathtt{T}$»-->

1. `new() -> Set` - creates an empty set.
2. `new(List) -> Set` - creates a set from the given list of elements. If the list contains duplicating elements, ignores them.
3. `size(Set) -> Nat` - returns the number of elements in the set.
4. `insert(Set, T) -> Set` - adds an element of type `T` to the set.
5. `union(Set, Set) -> Set` - computes the union of two sets.
6. `intersection(Set, Set) -> Set` - computes the intersection of two sets.
7. `difference(Set, Set) -> Set` - computes the difference of two sets. Note that this operation is not commutative.
8. `disjointUnion(Set, Set) -> Set` - computes the union of two sets. If the sets intersect, returns an error.
9. `contains(Set, T) -> Bool` - checks if an element is in the set.

<!--ᚦ«`disjointUnion` is a partial operation / a `Maybe Set` »-->

## Used in
1. Transaction (roots, actions)
2. Nullifier set

<!--ᚦ«These should be linked»-->

<!--ᚦ
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
page comments
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
«some minor fixes needed»
«make conversion to juvix or use stdlib»
«could we just use the stdlib?»
-->

# Nullifier set

The nullifier set interface requires two main operations:

1. `insert(NFSet, T) -> NFSet` - adds the nullifier of type T to the nullifier set.
2. `contains(NFSet, T) -> Bool` - searchers for the given element and returns `True` if the element was found.

At this point, this interface seems to be fully covered by the [[Set | set interface]].

!!! note
    For the future versions of the nullifier set:

        1.`Contains` should perform the check in O(1)
        2. The data structure should support proofs of non-existence



The nullifier set interface requires two main operations:

- `Insert(NFSet, T) -> NFSet` - adds the nullifier of type T to the nullifier set.
- `Contains(NFSet, T) -> Bool` - searchers for the given element and returns `True` if the element was found. 

At this point, this interface seems to be fully covered by the [set interface](./set.md).

!!! note
    For the future versions of the nullifier set:

    - `Contains` should perform the check in O(1)
    - The data structure should support proofs of non-existence


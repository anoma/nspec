# Map

Map is a structure that contains pairs (key: value), where key is of type `K` and value is of type `V`.

## Interface

1. `new() -> Map`
2. `add(Map, K, V) -> Map`
3. `size(Map) -> Nat`
4. `get(Map, K) -> V`
5. `keys(Map) -> List K`

<!--ᚦ«
Is the order of the keys relevant?
Could it be `Set K` instead of `List K` in the lat point?
»-->

# Used in
1. Action: `applicationData`
2. Action: `proofs`

<!--ᚦ«These should be linked»-->

<!--ᚦ
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
page comments
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
«Could we just use juvix maps?»
-->

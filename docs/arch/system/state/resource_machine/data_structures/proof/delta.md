## Delta proof inputs and constraints

### Instance

|Name|Type|Description|
|-|-|-|
|`delta`|`DeltaHash`|Transaction delta (computed from compliance unit deltas by adding them together)
|`expectedBalance`|`Balance`| Balanced transactions have delta pre-image 0 for all involved kinds

### Witness

1. Resource delta pre-images


### Constraints

1. `delta = sum(unit.delta() for unit in action.units for action in tx)` - can be checked outside of the circuit since all values are public
2. `delta`'s preimage's quantity component is `expectedBalance`


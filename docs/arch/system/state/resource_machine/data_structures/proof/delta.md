## Delta proof inputs and constraints

### Instance

|Name|Type|Description|
|-|-|-|
|`delta`|`DeltaHash`|Transaction delta (computed from compliance unit deltas by adding them together)

### Witness

TBD (openings of resource deltas?)

### Constraints

TBD: Transaction delta is correctly computed from the resource deltas
1. `delta = sum(unit.delta() for unit in action.units for action in tx)` - can be checked outside of the circuit since all values are public
2.
# NewQuorums


- _from_ [[Executor]]

##### Purpose

<!-- --8<-- [start:purpose] -->
Informs primaries about the quorums to use for a range of heights.
<!-- epochs? see https://github.com/anoma/specs/issues/180  -->
<!-- --8<-- [end:purpose] -->

##### Structure


| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [[Common types#allofthem|ChainId]] | the chain Id |
| `quorums` | [[Common types#allofthem|Quorums]] | the chain quorums |
| `start_height` | [[Common types#allofthem|Height]] | start height |
| `end_height` | [[Common types#allofthem|Height]] | end height |

##### Effects


The new learner graph structure is known.

##### Triggers


_none_

<!--
```rust
struct NewQuorums {
  chain_id : ChainId,
  quorums : Quorums,
  start_height : Height,
  end_height : Height,
}
```
-->

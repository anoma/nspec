---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### NewQuorums

<!-- --8<-- [start:purpose] -->
- _from_ [Executor]()

#### Purpose

Informs primaries about the quorums to use for a range of heights.
<!-- epochs? see https://github.com/anoma/specs/issues/180  -->
<!-- --8<-- [end:purpose] -->
<!-- --8<-- [start:details] -->

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [ChainId](./../types/allofthem/index.md#ChainId) | the chain Id |
| `quorums` | [Quorums](./../types/allofthem/index.md#Quorums) | the chain quorums |
| `start_height` | [Height](./../types/allofthem/index.md#Height) | start height |
| `end_height` | [Height](./../types/allofthem/index.md#Height) | end height |

#### Effects

The new learner graph structure is known.

#### Triggers

_none_

<!-- --8<-- [end:details] -->
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
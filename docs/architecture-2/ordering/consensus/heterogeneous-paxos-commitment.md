---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### `HPaxosCommitment`

<!-- --8<-- [start:purpose] -->
- _from_ [Consensus](../consensus-homogeneous.md)

#### Purpose

Encodes a $\oneb$ / $\twoa$ message used to communicate the acceptor's commitment to other acceptors.
<!-- --8<-- [end:purpose] -->
<!-- --8<-- [start:details] -->
The message is sent between the participating acceptor nodes.

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `height` | `Height` | height of the block |
| `timestamp` | `ClockTime` ||
| `proposal` | `NarwhalBlock` | proposed value |

!!! todo

    should this also include some kind of Hash representing who the proposer thinks the current  "quorums" are? That would ensure some kind of double-check, but may not be necessary...

#### Triggers

- to [Consensus](#Consensus): [`HPaxosCommitment`](#HPaxosCommitment)
- to [Mempool](#Mempool): [`RequestProposal`](#RequestProposal)
- to [Execution shards](#Shards): [`AnchorChosen`](#AnchorChosen)

<!-- --8<-- [end:details] -->
<!---
```rust
struct DirectReferences {
  chain_id : ChainId,
  height : Height,
  refs : Vec<Hash>,
}
```
-->

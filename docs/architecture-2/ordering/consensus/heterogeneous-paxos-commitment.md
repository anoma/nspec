### `HPaxosCommitment`

- _from_ [Consensus](../consensus-v1.md)

#### Purpose
<!-- --8<-- [start:purpose] -->
Encodes a $\oneb$ / $\twoa$ message used to communicate the acceptor's commitment to other acceptors.
<!-- --8<-- [end:purpose] -->
The message is sent between the participating acceptor nodes.

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `height` | `Height` | height of the block |
| `timestamp` | `ClockTime` ||
| `proposal` | `NarwhalBlock` | proposed value |

<!-- **TODO** should this also include some kind of Hash representing who the proposer thinks the current  "quorums" are? That would ensure some kind of double-check, but may not be necessary... -->

#### Triggers

- to [Consensus](#Consensus): [`HPaxosCommitment`](#HPaxosCommitment)
- to [Mempool](#Mempool): [`RequestProposal`](#RequestProposal)
- to [Execution shards](#Shards): [`AnchorChosen`](#AnchorChosen)

<!---
```rust!
struct DirectReferences {
  chain_id : ChainId,
  height : Height,
  refs : Vec<Hash>,
}
```
-->

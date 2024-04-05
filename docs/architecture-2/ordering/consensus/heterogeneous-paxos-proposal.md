### `HPaxosProposal`

- _from_ [Consensus](../consensus-v1.md)

#### Purpose
<!-- --8<-- [start:purpose] -->
Encodes a $\onea$-message that proposes a next value to have consensus upon.
<!-- --8<-- [end:purpose] -->
The message is sent between the participating acceptor nodes.

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `height` | `Height` | height of the block |
| `refs` | [`Vec<Hash>`](#Hash) | hashes of messages seen by the acceptor recently |
| `prev` | [`Hash`](#Hash) | hash of the previous message sent by acceptor, `0` otherwise |

!!! todo 

    should this also include some kind of Hash representing who the proposer thinks the current  "quorums" are? That would ensure some kind of double-check, but may not be necessary...

#### Triggers

- to [Consensus](../consensus-v1.md): [`HPaxosCommitment`](./heterogeneous-paxos-commitment.md)
- to [Mempool](#Mempool): [`CheckProposal`](#CheckProposal)

<!---
```rust
struct Proposal {
  chain_id : ChainId,
  height : Height,
  timestamp : ClockTime,
  proposal : NarwhalBlock,
  // should this also include some kind of Hash representing who the proposer thinks the current
  // "quorums" are? That would ensure some kind of double-check, but may not be necessary...
}
-->

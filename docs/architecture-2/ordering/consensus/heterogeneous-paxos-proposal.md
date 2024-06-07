---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### `HPaxosProposal`

<!-- --8<-- [start:purpose] -->
- _from_ [Consensus](../consensus-v1.md)

#### Purpose

Encodes a $\onea$-message that proposes a next value to have consensus upon.
<!-- --8<-- [end:purpose] -->
<!-- --8<-- [start:details] -->
The message is sent between the participating acceptor nodes.

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `timestamp` | `ClockTime` ||
| `height` | `Height` | height of the block |
| `proposal` | `NarwhalBlock` | proposed value |

<!-- !!! todo

    should this also include some kind of Hash representing who the proposer thinks the current  "quorums" are? That would ensure some kind of double-check, but may not be necessary...
-->

We define the _ballot_ of an `HPaxosProposal` message $B(m)$ to be the pair $\left\langle\textrm{timestamp}, \textrm{signature of }m\right\rangle$ (or some order-preserving Nat encoding thereof).
This ensures that `HPaxosProposal` ballot numbers are unique, and when proposed by honest proposers, they increase with time (which is useful for liveness). 

#### Triggers

- to [Consensus](../consensus-v1.md): [`HPaxosCommitment`](./heterogeneous-paxos-commitment.md)
- to [Mempool](#Mempool): [`CheckProposal`](#CheckProposal)

<!-- --8<-- [end:details] -->
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

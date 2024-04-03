### `PotentialProposal`

- _from_ [Mempool Primary](../mempool/primary.md)

#### Purpose
<!-- --8<-- [start:purpose] -->
Communicates that a specific payload is (or isn't) a valid proposal for consensus on the chain, which consensus might decide upon.
<!-- --8<-- [end:purpose] -->

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain ID |
| `payload` | [`NarwhalBlock`](#NarwhalBlock) | potential consensus value |
| `valid` | `bool` | indicates if the value is valid for consensus proposal |

#### Effects

- The valid payload value received in `PotentialProposal` is a potential value to be proposed (1A message).
- Having received a proposal (1A) message with this payload, the acceptor can now send a commitment (1B) message.

#### Triggers

- to [Consensus](#Consensus): [`HPaxosProposal`](#HPaxosProposal)

<!--
```rust
/// Communicates that a specific payload is (or isn't) a valid proposal for consensus on the chain.
struct PotentialProposal {
  chain_id : ChainId,
  payload : NarwhalBlock,
  valid : bool,
}
```
-->

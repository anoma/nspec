### AnchorChosen

- _from_ [Consensus](../../consensus-v1.md)

#### Purpose
<!-- --8<-- [start:purpose] -->
Inform shards about the most recently decided value by the consensus.
<!-- --8<-- [end:purpose] -->

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `learner` | `Learner` | learner |
| `height` | `Height` | height of the block |
| `anchor` | `NarwhalBlock` | the value that consensus decided upon |

#### Effects
The shard learns more ordering information. In particular, with this and enough `TimestampOrderingInformation` messages, it should be able to order all transactions before the new `anchor`.

!!! todo
  
    I guess, we need a proper talk on how to represent partial dependencies.

Once a we have enough ordering information to establish the unique write preceding a key on which there is a read lock, and we have a value for that write, we can send that value to the relevant Executor.

#### Triggers

- to [Executor](../executor.md): [`KVSRead`](../executor/KVS-read.md)
  `for each` locked key for which we have established a unique write value,
  send a `KVSRead` message to the appropriate Executor <!-- ‼ and once more capitalization .. -->

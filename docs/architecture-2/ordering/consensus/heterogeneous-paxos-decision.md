---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### `HPaxosDecision`

<!-- --8<-- [start:purpose] -->
- _from_ [Consensus](../consensus-v1.md)

#### Purpose

The message is used to notify other acceptors that a decision has been made.
<!-- --8<-- [end:purpose] -->
<!-- --8<-- [start:details] -->
The message includes a list of messages the other acceptors need to see the decision (a quorum of $\twoa$ messages).
Once the acceptor have received one of the decision messages for all learners, it may stop doing any kind of interesting consensus work,
and just send these out to anyone who is still trying to do consensus.

#### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `learner` | `Learner` | learner instance |
| `message_quorum` | [`Vec<DirectReference>`] | direct references to a quorum of messages |

#### Triggers

- to [Mempool](#Mempool): [`RequestProposal`](#RequestProposal)
- to [Execution shards](#Shards): [`AnchorChosen`](#AnchorChosen)

<!-- --8<-- [start:details] -->
<!---
```rust
struct Decision {
  // This is more of an optimization: sometimes it's helpful to tell someone that a decision has
  // been made, and send over the list of messages they need to see the decision (a quorum of 2As).
  // Note that once you have one of these for all learners, you can really stop doing any kind of
  // interesting consensus work, and just send these out to anyone who is still trying to do
  // consensus.
  learner : Learner,
  refs : DirectReferences,
-->

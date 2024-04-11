---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### `HeterogeneousPaxosMessage`

- _from_ [Consensus](#Consensus)

#### Purpose

<!-- --8<-- [start:purpose] -->
Intra-component message according to the consensus protocol, sent between the participating acceptor nodes.
<!-- --8<-- [end:purpose] -->

#### Structure

There are three variants of the message, dependent on the message purpose according to the [protocol specification]().

##### `HeterogeneousPaxosMessage`

```rust
enum HeterogeneousPaxosMessage {
  /// encodes a 1A
  HpmProposal(SignedMessage<Proposal>),
  /// encodes 1B, or (possibly multiple) 2As (for multiple learners)
  Hpm(SignedMessage<DirectReferences>),
  /// encodes decision notification message
  HpmDecision(SignedMessage<Decision>),
}
```

##### `Proposal` structure

Encodes a $\onea$ message that proposes a next value to have consensus upon.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `height` | `Height` | height of the block |
| `timestamp` | `ClockTime` ||
| `proposal` | `NarwhalBlock` | proposed value |

!!! todo

    should this also include some kind of Hash representing who the proposer thinks the current  "quorums" are? That would ensure some kind of double-check, but may not be necessary...

##### `DirectReferences` structure

Encodes a $\oneb$ / $\twoa$ message used to communicate the acceptor's commitment to other acceptors.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chain_id` | [`ChainId`](#ChainId) | the chain Id |
| `height` | `Height` | height of the block |
| `refs` | [`Vec<Hash>`](#Hash) | hashes of messages seen by the acceptor recently |
| `prev` | [`Hash`](#Hash) | hash of the previous message sent by acceptor, `0` otherwise |

##### `Decision` structure

The message of this kind is used to notify other acceptors that a decision has been made.
The message includes a list of messages the other acceptors need to see the decision (a quorum of 2A messages).
Once the acceptor have received one of the decision messages for all learners, it may stop doing any kind of interesting consensus work,
and just send these out to anyone who is still trying to do consensus.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `learner` | `Learner` | learner instance |
| `message_quorum` | `DirectReferences` | direct references to a quorum of messages |

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

struct DirectReferences {
  chain_id : ChainId,
  height : Height,
  refs : Vec<Hash>,
}

struct Decision {
  // This is more of an optimization: sometimes it's helpful to tell someone that a decision has
  // been made, and send over the list of messages they need to see the decision (a quorum of 2As).
  // Note that once you have one of these for all learners, you can really stop doing any kind of
  // interesting consensus work, and just send these out to anyone who is still trying to do
  // consensus.
  learner : Learner,
  refs : DirectReferences,
}
```
-->

#### Triggers

- to [Consensus](#Consensus): [`HeterogeneousPaxosMessage`](#HeterogeneousPaxosMessage)
- to [Mempool](#Mempool): [`CheckProposal`](#CheckProposal), [`RequestProposal`](#RequestProposal)
- to [Execution shards](#Shards): [`AnchorChosen`](#AnchorChosen)

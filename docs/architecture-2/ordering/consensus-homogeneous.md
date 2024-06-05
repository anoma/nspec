---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# (Homogeneous) Consensus

## Introduction

### Purpose
Consensus component establishes a totally ordered sequence of headers received from the [mempool](mempool.md) DAG.
This establishes a total order of transactions for the [execution engine](execution.md) to execute.

### Background

The consensus algorithm is based on [Heterogeneous Paxos](https://arxiv.org/abs/2011.08253).
It incorporates optimizations from the Heterogeneous Paxos 2.0 ART report, [a draft of which can be found here](https://www.dropbox.com/scl/fi/msxr901ipaqv64f9wjbhg/ART_HPaxos_2-2.pdf?rlkey=7m837xzamnfwh7cks7k5nsxy4&dl=0).
Here we adapt for the homogeneous case, in which there is only one _learner_. 

### Scope

## Overview

The protocol involves two kinds of agents: _proposers_ and _acceptors_.
Each validator may play the role of any combination of the two kinds of agents.

**Proposer** initiate a round by a proposing a value to agree upon.
We denote a set of possible consensus values $\Value$.

**Acceptors** are agents who agree on the proposed values and an agent may be acceptor for more than one chain (instance).
No correct acceptor acts on any _invalid_ decided value.
This requires that proposals can be checked for validity.
Non-byzantine correct acceptors are also called _honest_, _safe_, or _real_.

**Learners** are agents who are interested in values decided by consensus on particular chains.
As this is a Homogeneous Paxos, all learners are interested in only one chain, and make the same failure assumptions. 
Their quorums are determined by the chain's protocol (e.g. proof of stake).

## Functionality

Acceptors need to are aware of the learners and their quorums. __TODO__

Values are agreed upon in rounds.

<!-- Next, we describe how the communication for a consensus round works. -->
### Informal protocol round description

Consensus rounds send and receive messages in four (possibly overlapping) phases:

1. proposing the consensus value $v \in \Value$
2. acknowledging receipt of proposals
3. establishing consensus
4. termination

The first three phases correspond to three types of intra-component messages: $\onea$, $\oneb$ and $\twoa$, respectively.

Before processing a received message $m$, acceptors and learners check if the message is [_wellformed_](consensus/hpaxos-formal.md#definition-wellformed).
The formal definition of the wellformedness relation, denoted by $\wellformed{m}$, is given [here](consensus/hpaxos-formal.md).
Non-wellformed messages are rejected.
The acceptors caught in sending non-wellformed messages might be punished by the protocol.

<!-- Suppose we have two learners $l_\alpha$ and $l_\beta$ which refer to agents that are interested in blockchain $\alpha$ and blockchain $\beta$. -->

#### $\onea$-message: proposing a value

Proposer proposes a next value by sending a $\onea$-message to the acceptors.
The message carries a _unique_ ballot value, containing the proposed value to agree on and the round timestamp (round number).
We assume that the set of all possible ballot values is linearly ordered.

#### $\oneb$-message: acknowledging receiving the proposal

On receipt of a $\onea$-message, an acceptor sends an acknowledgement of its receipt to all other acceptors and learners in the form of $\oneb$-message.

#### $\twoa$-message: establishing consensus

When an acceptor receives $\oneb$ messages for the highest ballot number it has seen
from a <!-- learner $l_\alpha$’s --> [quorum](consensus/hpaxos-formal.md#definition-quorums-in-messages) of acceptors,
it sends a $\twoa$-message.
<!-- labeled with $l_\alpha$. -->

However, there is one restriction:
once a safe acceptor has sent a $\twoa$-message $m$, <!-- for a learner $l_\alpha$ --> it
never sends a $\twoa$-message with a different value for a learner $l_\beta$, unless one of the following is true: __TODO__

- It knows that a quorum of acceptors has seen a quorum of $\twoa$-messages with learner $l_\alpha$ and ballot number higher than $m$.
- It has seen Byzantine behavior that proves $l_\alpha$ and $l_\beta$ do not have to agree.

The acceptor who has received a $\oneb$ sends a $\twoa$ for every learner for which it can produce a wellformed $\twoa$.

#### Termination: finalizing consensus value

A learner <!-- $\red{l_\alpha}$ --> decides on a value $v \in \Value$ when it receives a set <!-- $\red{q_\alpha}$ --> $\red{q}$ of $\twoa$-messages <!-- labeled with $l_\alpha$ --> with
the same proposed value $v$ and ballot $b$ from one of its quorums of acceptors.
We call such a set a _decision_. <!-- and write $\decision{\red \alpha}{b, \red{q_\alpha}}$. -->

If no decision can be reached within a certain time, proposers must begin a new round (with a higher timestamp, and thus a higher ballot).
Proposers can start a new round by proposing a new value or by trying to finalize the same value again (in case there was no consensus).

In general, acceptor relay all sent or received messages to <!-- all learners --> the learner and all other acceptors.
This ensures that any message received by a real acceptor is received by all real acceptors and the learner.

#### Protocol message structure

Any $\oneb$ and $\twoa$-message $m$ signed by the acceptor $A$ has the following fields:

- `prev` — a reference to the previous message sent by $A$, if such exists.
- `refs` — a set of hashes of message referenced by $m$. They are the messages that $A$ has received since between sending $m$ and the previous to $m$ message, including the previous message itself.
<!-- - `lrn` — a learner tag: an identifier of the relevant chain (for $\twoa$-messages only). -->

To ensure that acceptors and learners _fully understand_ each message they receive, they delay doing any computation on it (sometimes called delivery) until they have received all the messages in `refs`.
As a result, acceptors and learners will always process messages from any given sender in the order they were sent, but also from any messages that sender received, and recursively.

### Pseudocode

We assume that there is a way to assign to every wellformed message $m$ a unique ballot number that the message belongs to.
We shall denote the ballot number assigning function as $\ba{m}$.
The formal definition of the function can be found [here](consensus/hpaxos-formal.md#definition-ballot-numbers).

We assume that every acceptor maintains an internal state with the following structures:

- `known_messages` — a set of all processed messages, initially empty;
- `recent_messages` — a set of all messages the acceptor has sent or received since (and including) the last message it sent, initially empty;
- `previous_message` — the most recent message the acceptor has sent, is such exists, initially special non-message value.

```python
def init():
    known_messages = {}
    recent_messages = {}
    previous_message = NON_MESSAGE

def process_message(m):
    # ignore messages that have been already processed
    if m in known_messages:
        return

    # forward message to all acceptors and learners
    broadcast(m)

    known_messages.insert(m)
    recent_messages.insert(m)

    if m.type == "1a":
        new_1b = 1b(prev = previous_message, refs = recent_messages)
        recent_messages = {}
        previous_message = new_1b
        process_message(new_1b)

    else if m.type == "1b" and B(m) == max ([B(x) for x in known_messages]):
        foreach learner in Learner:
            new_2a = 2a(prev = previous_message, refs = recent_messages, lrn = learner)
            if WellFormed(new_2a):
                recent_messages = {}
                previous_message = new_2a
                process_message(new_2a)

def run():
    # initialize state
    init()

    # main loop
    while True:
        m = deliver_next_wellformed_message()
        # the function must guarantee that:
        # 1) the messages are delivered in the order they were sent, i.e.,
        assert foreach r in m.refs: r in known_messages
        # holds, and
        # 2) the delivered messages are wellformed

        process_message(m)
```

### Efficient Implementation

The efficient implementation of consensus is described [here](consensus/hpaxos-eff.md).

## Communication diagram

<!-- Diagram illustrating message flows between engines -->

## Messages Received

Below is the specification of the consensus component in terms of all the messages the component must be able to receive and react to.

### [PotentialProposal](consensus/potential-proposal.md)

from [Mempool Primary](./mempool/primary.md) may trigger:

- `HPaxosProposal` → Consensus
  --8<-- "consensus/heterogeneous-paxos-proposal.md:purpose"

### [HPaxosProposal](consensus/heterogeneous-paxos-proposal.md)

from [Consensus](consensus.md) may trigger:

- `HPaxosCommitment` → Consensus
  --8<-- "consensus/heterogeneous-paxos-commitment.md:purpose"
- `CheckProposal` → Mempool Primary
  --8<-- "mempool/primary/check-proposal.md:purpose"

### [HPaxosCommitment](consensus/heterogeneous-paxos-commitment.md)

from [Consensus](consensus.md) may trigger:

- `HPaxosCommitment` → Consensus
  --8<-- "consensus/heterogeneous-paxos-commitment.md:purpose"
- `RequestProposal` → Mempool Primary
  --8<-- "mempool/primary/request-proposal.md:purpose"
- `AnchorChosen` → Execution Shards
  --8<-- "execution/shard/anchor-chosen.md:purpose"

### [HPaxosDecision](consensus/heterogeneous-paxos-decision.md)

from [Consensus](consensus.md) may trigger:

- `RequestProposal` → Mempool Primary
  --8<-- "mempool/primary/request-proposal.md:purpose"
- `AnchorChosen` → Execution Shards
  --8<-- "execution/shard/anchor-chosen.md:purpose"

### [NewQuorums](consensus/new-quorums.md)

from [Executor](./execution/executor.md) may trigger: _none_

## Example scenario

<!-- Short message cascade from a typical common message sent to the machine  -->
<!-- E.g. an example of the common case "life of a transaction or whatever" flow from inputs to outputs -->

## Further reading


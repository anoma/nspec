---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# (Homogeneous) Consensus

## Introduction

### Purpose

Consensus establishes a totally ordered sequence of headers received from the [mempool](mempool.md) DAG.
This establishes a total order of transactions for the [execution engine](execution.md) to execute.

### Background

The consensus algorithm is based on [Heterogeneous Paxos](https://arxiv.org/abs/2011.08253).
It incorporates optimizations from the [Heterogeneous Paxos 2.0 ART report](https://art.anoma.net/),
[a draft of which can be found here](https://www.dropbox.com/scl/fi/msxr901ipaqv64f9wjbhg/ART_HPaxos_2-2.pdf?rlkey=7m837xzamnfwh7cks7k5nsxy4&dl=0).
Here we adapt for the homogeneous case, in which there is only one _learner_.

### Scope

The Consensus Engine is responsible for establishing a total order on transaction candidates produced by the [mempool](mempool.md).

We start by describing the consensus protocol informally, as well as the protocol trust model for the homogeneous case and the desired properties.
Finally, we provide a pseudocode for its agents.

The necessary formal definitions are given in the [dedicated page](consensus/homogeneouspaxos-formal.md).

## Overview

The protocol involves three kinds of agents: _proposers_, _acceptors_, and _learners_.
Each validator may play the role of any combination of the two kinds of agents.

__Proposers__ initiate a round by a proposing a value to agree upon.
We denote a set of possible consensus values $\Value$.

__Acceptors__ are agents who actually perform the consensus protocol (sending and receiving messages).
No correct acceptor acts on any _invalid_ decided value.
This requires that proposals can be checked for validity.
Non-byzantine correct acceptors are also called _honest_, _safe_, or _real_.

__Learners__ are agents who are interested in values decided by consensus (they only need to receive messages).
As this is a Homogeneous Paxos, all learners and acceptors are interested in only one chain, and make the same failure assumptions. 
Their quorums are determined by the chain's protocol (e.g. proof of stake).
We denote the set of learners by $\Learner$.
In the homogeneous case, the set of learners is a singleton, $\Learner = \cb{\red\alpha}$.

## Trust Model

For the homogeneous case, learner $\red\alpha$ is characterized by 2 sets: _quorums_ $Q_{\red\alpha}$ and _safe sets_ $\Safe{\red\alpha}$.

### Reality

We call the unknown set of acceptors who are actually _live_ (will always eventually send a message according to the protocol) $\reallylive$.
Other acceptors may be called _unlive_, _crash-prone_, or just _crashed_.

We call the unknown set of acceptors who are actually _safe_ (will never send messages other than those specified by the protocol) $\reallysafe$.
Other acceptors may be called _unsafe_ or _Byzantine_. 

The learner $\red\alpha$ does not send any messages according to the protocol, so it's not meaningful to talk about it being live or safe.

Unfortunately, no one knowns $\reallylive$ and $\reallysafe$, so we now characterize the assumptions $\red\alpha$ must make
in order to get safety and liveness guarantees.

### Quorums

A [quorum](https://en.wikipedia.org/wiki/Quorum_(distributed_computing)) is a set of acceptors sufficient to make $\red\alpha$ decide.
Whenever any quorum remains safe and live, $\red\alpha$ should _eventually_ reach a decision.
Quorums are determined by chain policy (e.g., proof of stake).
We designate the set of quorums $Q_{\red\alpha}$ (so each element of $Q_{\red\alpha}$ is a set of acceptors).
In general, for any quorum $q_{\red\alpha} \in Q_{\red\alpha}$, any superset of acceptors is also a quorum (adding more safe and live acceptors doesn't make $\red\alpha$ no longer able to decide).
Formally,

$$
  \forall q \in Q_{\red\alpha}.\,
  \forall q^\prime \supseteq q.\,
  q^\prime \in Q_{\red\alpha}
$$

### Safe Sets

In general, the learner $\red\alpha$  wants its decision to _agree_: if it makes two decisions, they should carry the same value.
Unfortunately, there is no way to ensure $\red\alpha$ both liveness (it eventually decides) and agreement, under all conditions.
_Safe sets_ $\Safe{\red\alpha}$ characterize when $\red\alpha$ is guaranteed agreement.
Each safe set is a set of acceptors, and $\red\alpha$ is guaranteed agreement when at least one safe set consists entirely of safe (if not necessarily live) acceptors.
Like quorums, adding more safe acceptors doesn't hurt $\red\alpha$'s guarantees:

$$
  \forall s \in \Safe{\red\alpha}.\,
  \forall s^\prime \supseteq s.\,
  s^\prime \in \Safe{\red\alpha}
$$

Safe sets and quorums are related: Paxos requires that all quorums intersect on a safe acceptor to guarantee agreement.
Therefore we require:

$$
  \forall q, q^\prime \in Q_{\red\alpha}.\,
  \forall s \in \Safe{\red\alpha}.\,
  q \cap q^\prime \cap s \ne \emptyset
$$

For many systems (including most proof of stake systems), the safe sets are simply all sets with this property.

### Desired Properties

Paxos ultimately guarantees that if a quorum is safe and live ($\reallylive \cap \reallysafe \in Q_{\red\alpha}$), the learner $\red\alpha$ eventually decides.

Paxos also guarantees that if a safe set is safe ($\reallysafe \in Q_\red{\alpha}$), all decisions the learner $\red\alpha$ makes have the same value.

### Accurate

We say that learner $\red\alpha$ is _accurate_ if its decisions must agree.

$$
  \accurate{\red\alpha} \eqdef \reallysafe \in Q_\red{\alpha}
$$

## Functionality

All agents know $\Safe{\red\alpha}$ and $Q_{\red\alpha}$.

Each anchor vertex is decided using an independent instance of consensus.
This could be referred to as the "separate consensus for each height" approach.

Here we discuss the workings of a single consensus instance, parameterized by some height.
The possible values $\Value$ are therefore vertices from the Mempool.
The decided vertex becomes the anchor vertex for this height.

Within the consensus instance, values are agreed upon in rounds.

<!-- Next, we describe how the communication for a consensus round works. -->
### Informal protocol round description

Consensus rounds send and receive messages in four (possibly overlapping) phases:

1. proposing the consensus value $v \in \Value$
2. acknowledging receipt of proposals
3. establishing consensus
4. termination

The first three phases correspond to three types of intra-component messages: $\onea$, $\oneb$ and $\twoa$, respectively.

Before processing a received message $m$, acceptors and learners check if the message is [_wellformed_](consensus/homogeneouspaxos-formal.md#definition-wellformed).
The formal definition of the wellformedness relation, denoted by $\wellformed{m}$, is given [here](consensus/homogeneouspaxos-formal.md).
Non-wellformed messages are rejected.
The acceptors caught in sending non-wellformed messages might be punished by the protocol.

<!-- Suppose we have two learners $l_\alpha$ and $l_\beta$ which refer to agents that are interested in blockchain $\alpha$ and blockchain $\beta$. -->

#### 1a-message: proposing a value

A proposer proposes a next value by sending a $\onea$-message to the acceptors.
The message carries a _unique_ ballot value, containing the proposed value to agree on and the round timestamp (round number).
We assume that the set of all possible ballot values is linearly ordered.

Proposers can safely propose any value at any time. 
However, the learner $\red\alpha$ will reach a decision more quickly if a proposal has a higher ballot than previous proposals, and a value that agrees with recent $\twoa$-messages.

#### 1b-message: acknowledging receiving the proposal

On receipt of a $\onea$-message, an acceptor sends an acknowledgement of its receipt to all other acceptors and learners in the form of $\oneb$-message.

#### 2a-message: establishing consensus

When an acceptor receives $\oneb$ messages for the highest ballot number it has seen
from a <!-- learner $l_\alpha$’s --> [quorum](consensus/homogeneouspaxos-formal.md#definition-quorums-in-messages) of acceptors,
it sends a $\twoa$-message.
<!-- labeled with $l_\alpha$. -->

However, there is one restriction:
once a safe acceptor has sent a $\twoa$-message $m$, <!-- for a learner $\red\alpha$ --> it
never sends a $\twoa$-message with a different value, <!-- for a learner $\blue\beta$ --> unless one of the following is true:

- It knows that a quorum of acceptors has seen a quorum of $\twoa$-messages with <!-- learner $\red\alpha$ and --> ballot number higher than $m$. (In which case we call $m$ "_buried_.")
- It has seen Byzantine behavior that proves $\red\alpha$ is not _accurate_, in which case decisions do not have to agree.

The acceptor who has received a $\oneb$ sends a $\twoa$ for every learner for which it can produce a wellformed $\twoa$.

#### Termination: finalizing consensus value

The learner $\red{\alpha}$ decides on a value $v \in \Value$ when it receives a set $q_\red{\alpha}$ of $\twoa$-messages <!-- labeled with $l_\alpha$ --> with
the same proposed value $v$ and ballot $b$ from one of its quorums of acceptors.
We call such a set a [_decision_](consensus/homogeneouspaxos-formal.md#definition-decision).  <!-- and write $\decision{\red \alpha}{b, \red{q_\alpha}}$. -->

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
The formal definition of the function can be found [here](consensus/homogeneouspaxos-formal.md#definition-ballot-numbers).

#### Broadcast
We assume a `broadcast` primitive that ensures that all messages sent or received by a safe and live agent are eventually received by all agents. 
One way to implement this is to have live agents echo messages received to all other live agents. 
More efficient implementations may involve explicit requests for unreceived messages referenced in other messages `refs` fields. 

#### Acceptors

We assume that every acceptor maintains an internal state with the following structures:

- `known_messages` — a set of all processed messages, initially empty;
- `recent_messages` — a set of all messages the acceptor has sent or received since (and including) the last message it sent, initially empty;
- `previous_message`  — the most recent message the acceptor has sent, is such exists, initially containing a special non-message value.

Below, we present the acceptor algorithm in pseudocode.

```python title="Acceptor algorithm"
def init():
  known_messages = {}
  recent_messages = {}
  previous_message = None

def process_1a(m):
  with z = 1b(prev = prev_message, refs = recent_messages ∪ {m}):
    if WellFormedOneB(z):
      recent_messages = {z}
      previous_message = z
      broadcast(z)

def process_1b(m):
  with z = 2a(prev = prev_message, refs = recent_messages ∪ {m}):
    if WellFormedTwoA(z):
      recent_messages = {z}
      previous_message = z
      broadcast(z)
    else:
      recent_messages.insert(m)

def process_2a(m):
  recent_messages.insert(m)

def process_message(m):
  if m not in known_messages:
    for r in m.refs:
      while not r in known_messages:
        wait()
    if WellFormed(m):
      known_messages.insert(m)
      if m.type == "1a":
        process_1a(m)
      if m.type == "1b":
        process_1b(m)
      if m.type == "2a":
        process_2a(m)
```
<!-- Note that we do not have a `process_2a` method, as the only thing we need to do is insert it in `known_messages` and `recent_messages`, which we do in `process_message`. -->

#### Learners

The learner algorithm in pseudocode is presented below.

```python title="Learner algorithm"
def init():
  known_messages = {}
  decision = None

def process_message(m):
  if not m in known_messages:
    for r in m.refs:
      while not r in known_messages:
        wait()
    if WellFormed(m):
      known_messages.insert(m)

def decide():
  foreach s in subsets(known_messages):
    if Decision(s):
      decision = V(s)
```

#### Proposers

For simplicity, we assume the same validators act as proposers and acceptors.
This ensures that if there is a safe and live acceptor, there is a safe and live proposer.
The proposers should be chosen in a round-robin fashion, with increasing time-outs.

One way to accomplish this is to include timestamps in the (most significant bits of) the ballot value of each proposal:

- We then allocate "time windows" to proposers according to some pre-determined function based on the state of the chain (perhaps based on the timestamp of the narwhal vertex chosen in the previous instance of consensus, for the previous height).
- These time windows cycle through all the proposers, with increasing duration (at least linearly, possibly exponentially, we can only know what schedule works best experimentally).
- Proposals with a time stamp outside a time window of their signer are not well-formed.
- All agents delay receipt of all proposals until their own clock matches or exceeds the time stamp of the proposal.
- During its time window, an agent proposes the value of the highest $\twoa$ its local acceptor knows (or a vertex from the mempool, if it knows no $\twoa$s).
- For reasons detailed in the original liveness proof from Heterogeneous Paxos, proposers should propose three times during their time window, equally spaced. If proposer clock skew is bounded (even if the bound is unknown), this guarantees the learner eventually decides.

As an optimization, proposers can stop proposing if they can produce a collection of messages that qualify as a _decision_, and then broadcast that to all learners.

```python title="Proposer algorithm"
def init(proposer_schedule) # determined for this height's consensus instance
  known_messages = {}
  schedule = proposer_schedule
  proposal_from_mempool = None
  restart_timer() 

def restart_timer()
  if exists s in subsets(known_messages) such that Decision(s):
    forall m in s:
      broadcast(m)
  else:
    window = my_first_time_window_after_now(schedule)
    start_timer(window.start, self.on_timeout)
    start_timer(window.start + (0.33 * window.duration), self.on_timeout)
    start_timer(window.start + (0.66 * window.duration), self.on_timeout)
    start_timer(window.start + (0.66 * window.duration), self.restart_timer)

def process_message(m):
  if WellFormed(m):
    known_messages.insert(m)

def receive_proposal_from_mempool(p):
  proposal_from_mempool = m

def on_timeout(last_known_timer):
  if exists m in known_messages and m.type == "2a":
    broadcast(
      argmax(lambda m : B(m), filter(lambda m: m has type 2a, known_messages))
    )
  elif proposal_from_mempool is not None:
     broadcast(proposal_from_mempool)
```

<!-- ### Efficient Implementation

The efficient implementation of consensus is described [here](consensus/hpaxos-eff.md). -->

## Communication diagram

<!-- Diagram illustrating message flows between engines -->

## Messages Received

Below is the specification of the consensus component in terms of all the messages the component must be able to receive and react to.

### [[PotentialProposal]]

--8<-- "consensus/potential-proposal.md:purpose"

<details markdown="1">
  <summary>Details</summary>
--8<-- "consensus/potential-proposal.md:details"
</details>

### [[HPaxosProposal]]

--8<-- "consensus/heterogeneous-paxos-proposal.md:purpose"

<details markdown="1">
  <summary>Details</summary>
--8<-- "consensus/heterogeneous-paxos-proposal.md:details"
</details>

### [[HPaxosCommitment]]

--8<-- "consensus/heterogeneous-paxos-commitment.md:purpose"

<details markdown="1">
  <summary>Details</summary>
--8<-- "consensus/heterogeneous-paxos-commitment.md:details"
</details>

### [[HPaxosDecision]]

--8<-- "consensus/heterogeneous-paxos-decision.md:purpose"

<details markdown="1">
  <summary>Details</summary>
--8<-- "consensus/heterogeneous-paxos-decision.md:details"
</details>

<!-- ## Example scenario -->

<!-- Short message cascade from a typical common message sent to the machine  -->
<!-- E.g. an example of the common case "life of a transaction or whatever" flow from inputs to outputs -->

## Further reading

1. Isaac Sheff, Xinwen Wang, Robbert van Renesse, and Andrew C. Myers. Heterogeneous Paxos: Technical Report, 2020.
2. Aleksandr Karbyshev, Isaac Sheff. Heterogeneous Paxos 2.0: the Specs, 2024.

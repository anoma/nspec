---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Consensus

- *Inputs*
    Consensus requests, consensus messages
- *Outputs*
    Consensus messages, consensus outputs (finalized)
- *Preferences*
    Whether to run a particular consensus round
- *Accounting*
    Consensi actually performed

---

# Heterogeneous Paxos

## Summary

This specification intends to describe how heteregenous Paxos can be realized in the blockchain context. Given well-defined quorums, the protocol allows a known set $S$   $(|S|\geq1)$ of chains to construct and  carry out atomic transactions on a so-called *chimera chain*, subject to certain conditions.  The chimera chain guarantees safety and liveness subject to the usual assumption: at most a third of the stake belongs to Byzantine participants.

The protocol involves three kinds of agents: proposers, acceptors and learners. A node may play the role of any combination of the three kinds of agents.

Blocks are agreed upon in rounds.

**Proposer** initate a round by a  proposing a block. Each block contains atomic batches of transactions (or even a single transaction). An atomic batch of transactions means that either all transactions in the batch are executed or none of them are executed.

**Acceptors** are agents who agree on the proposed blocks and an agent may be acceptor for more than one chain. No correct acceptor acts on any invalid block. This requires checking the validation of blocks or state transition function.

**Learners** are set of agents where this set is intrested in a particualar (combination of?) chain(s) meaning what the voting process decides for these chain(s). The definition of learners is based on the quorums and defined by the protocol, meaning that agents are not free not choose their own quorum setups. <!--For example, there might be three well-defined learners $l_x$ and $l_y$, and $l_xy$ which are agents who are interetsted in chain $x$ alone, chain $y$ alone, and both chain $x$ chain $y$.--> Acceptors need to be aware of the different definitions of learners in order to be able to know what correct behavior is defined as. This set of the agents for learners, might empty or have overlaps, the acceptors have to follow the deifnition regardless. <!--Acceptor of chain are considered also part of learners of that chain.-->

We briefly describe how the communication for a consensus round works. Suppose we have two learners $l_x$ and $l_y$ which refer to agents that are interested in blockchain $x$ and blockchain $y$. Proposers propose a chimera block, by sending $1a$ messages, each carrying a value and unique ballot number (round identifier), to acceptors. All acceptors in all involved chains ($S$) send $1b$ messages to each other to communicate that they’ve received a $1a$ message. When an acceptor receives a $1b$ message for the highest ballot number it has seen from a learner $l_x$’s quorum of acceptors, it sends a $2a$ message labeled with $l_x$ and that ballot number. There is one exception: once a safe acceptor sends a $2a$ message $m$ for a learner $l_x$, it never sends a $2a$ message with a different value for a learner $l_y$, unless one of the following is true:
* It knows that a quorum of acceptors has seen $2a$ messages with learner $l_x$ and ballot number higher than $m$.
* It has seen Byzantine behavior that proves $l_x$ and $l_y$ do not have to agree.

A learner $l_x$ decides on a block when it receives $2a$ messages with the same proposed block and ballot number from one of its quorums of acceptors.

## Preliminaries

- _Base chains_ are two or more independent chains between which we would like to carry out atomic transactions. The chains must protocol-wise adhere to some  specific set of requirements to be compatible. For example, IBC support.
<!-- These chains are programmed with chimera chains in mind: for example, they may all be Anoma chains. -->

- A _chimera chain_ is a chain that allows atomic transactions to be carried out on [objects](https://en.wikipedia.org/wiki/Object_(computer_science)) from the base chains. It carries an additional consensus mechanism, that is dependent on the consensus of the base chains.

- A _learner_ is a client that is interested in the value decided by the voting process. Learners might be full nodes, light client nodes, or nodes from other chains.

- An _acceptor_ is an agent participating in the voting process of the consensus protocol. Non-byzantine acceptors are called _real_ acceptors.

<!--We denote a set of acceptors by `Acceptor`.-->

- A _quorum_ is a subset of acceptors sufficient to make a learner decide on a value. For a learner to maintain consistency (avoid deciding on two contradictory values), any two of its quorums must have a common real acceptor. Most chains achieve this practically by making the intersection of the quorums big enough, i.e. the acceptors in the intersection being backed by more than >1/3 stake of each chain under <1/3 Byzantine assumption. For example, suppose:
    - Base chain A has a total stake of $60 Astake$.
    - Base chain B has a total stake of $300Bstake$.
    - Any set of acceptors backed by $>40Astake$ is a quorum of chain A. This means $>20 Astake$ would have to back unsafe acceptors for chain A to fork.
    - Any set of acceptors backed by $>200Bstake$ is a quorum of chain B. This means $>100Bstake$ woudl have to back unsafe acceptors for chain B to fork.
    - Suppose that, for every quorum $q_a$ of chain A, and every quorum $q_b$ of chain B, the acceptors in $q_a\cap q_b$ are backed by $>10Astake$, and $>50 Bstake$. This would mean that, in order for atomic batches on the chimera chain to lose atomicity, $>10Astake$ and $>50Bstake$ would have to back unsafe acceptors.
        - When a batch loses atomicity, the transactions on one state machine (say, A) are executed, but not the transactions on the other state machine (say, B). However, each state machine itself remains consistent: neither A nor B forks.
        - This means some chimera chains offer atomicity with lower (yet well-defined) levels of integrity than their base chains' no-fork guarantees.

- A _proposer_ is an acceptor that may propose a new block according to the rules of the blockchain. For Typhon, the "blocks" of the consensus protocol are the headers produced by the [mempool](mempool.md#mempool). A potential proposer would need (a) data availability, (b) the ability to sign messages, ( c) something at stake (to prevent spam) and (d) the ability to communicate with the acceptors. Acceptors that are in the overlaps of quorums may especially well suited to be proposers, but other Acceptors (or even other machines) might be proposers as well.
 The Heterogeneous Paxos technical report effectively uses weighted voting for select proposer, but perhaps there are interesting tricks with VRFs that would improve efficiency.

### Assumptions

1. **Acceptors are staked**:  An acceptor has a certain amount of stake backing them. This stake is either fully their own stake or is partly delegated to them by other token holders.
2. **Quorums are known**: Quorums are defined implicitly by the internal logic of each chain. For most proof-of-stake chains, a quorum is a subset of acceptor that have $>\frac23$ of stake backing them.
3. **Large Overlap of Quorums**: A practical way to ensure a safe acceptors in the overlap between quorums. To guarantee atomicity with the same integrity as base chains, each quorum overlap must be backed by $>\frac13$ of the stake of each base chain.
4. **Connectivity**: All acceptors in a chimera chain communicate with each other (even if that means talking to acceptors who are not on the same base chain). This communication *can* be indirect (i.e. gossiping through other acceptors), so long as all pairs of honest acceptors can always communicate.
5. **Only one learner per main chain**: We model the learner graph as one learner per main chain, and then full nodes can instantiate their base chain's learner to make decisions. The reason is that in Heterogeneous Paxos the learner graph is a closed graph with known nodes, while in the blockchain context we have a open network where we don't know who all the learners are.

<!--
Formally,
$$
\forall q_1, q_2 : Quorum. \exists a : Acceptor. a \in q_1 \land a \in q_2 \land real(a)
$$
-->
## Chimera Chain

In this section we describe how chimera chains operate.

Upon wanting to include an atomic batch of transactions from the transaction pool into a block, a block proposer either creates a genesis block if there is no existing chimera chain or builds on top of an existing chimera chain.

### Genesis block

In order to be safe, the guarantee we want here is that future quorum updates on the main chains are guaranteed to be received before voting happens on chimera chains.

1. Create a genesis block that claims to be a "chimera chain" and allocate some unique name or index.
2. Register (in a transaction) that genesis block on all base chains and allocate it some unique name, so they know to involve it in any future quorum updates. The guarantee we want here is that future quorum updates are guaranteed to be received before votes happen.
3. The first block append on the chimera chain requires IBC messages from all base chains explaining that they have registered this genesis block.

### Producing Blocks

The block consists of transactions from both chains or just on of the chains. The transaction can be bundled together to make sure they are carried out atomically.

It is possible that more than one block may be finalized like in Grandpa (from Polkadot project) decoupling block prduction from finalization. In thi scase, Heterogeneous Paxos would serve the roll of a "finality gadget" in Grandpa's terms, but blocks could be produced at any rate.

#### Moving Objects

<!--A higher-level programming concept that might be more useful.-->

Suppose state in each state machine is expressed in terms of objects (think object-oriented programming) with state and methods, and a location (each is located on a chain).  Our ideas about "movable objects" should be applicable to any program entities which feature:
* a unique identifier
* a permanent set of public methods (an API) callable by users, or other methods on other objects in the same state machine, which can compute and return values
* a set of private methods callable only by other methods on this object
* mutable state (which only methods can mutate)

These are much like "smart contracts," which also carry internal mutable state and public APIs much like methods. An example of an "object" is any sort of account: multisignature account or single user account:
* accounts usually have a unique identifier
* public methods include "send money," which takes as input some signed authorization and deducts money from the account.
* mutable state includes some value representing the amount of money in the account.

One might want to move an object to another state machine. For simplicity, let's suppose it's a state machine with the same quorums (on a different, possibly chimera, chain). This is not so very different from various chains trying to get a lock on an account (objects) and then perform atomic operations on them.

This "move" operation should require an IBC send, and then deleting the original object. Or instead of deleting the original object the original object can be made a _pointer_ to the object which now lives primarily on the destination chain. On the destination state machine, an IBC receive should be followed by creating a new copy of the object. Any "object identifiers" found in pointers from other objects will have to be preserved, which could be tricky.

<!--
To implement moving objects in practice, the object can be locked on original chain upon being moved and only unlocked once it is moved back, when it can be updated. -->

##### Permissions for moving Objects

We have to consider who is allowed to move which objects where. One way to do this is to have "move" simply be a "private method" of any object: the programmer has to specifically program in any methods that the transactions or other objects can call to move the object. The most straightforward private method definition would allow anyone (e.g.,owners) who can control the object be able to give permission for moving. <!--While they can also define the private method to give this permission to any other object they control (e.g., smart contract). -->

We may want to allow chains to specify limits on what objects can move onto that chain. For example, they may require that objects have a method that can move them back to a base chain.

<!--This could get messy fast.-->

<!--Another possibility is to have each object specify its required safety and liveness properties, and then check with each move that these are preserved. This too could get messy. We may end up doing Information Flow Control.-->

## Epoch Change

<!--What happens when a main chain updates its quorums (moves to a new epoch)?

How is updating done?-->

If new quorums for each base chain do not overlap on a real acceptor, atomicity cannot be guaranteed. We can no longer meaningfully commit atomic batches to the chimera chain. However, extensions to the chimera chain are consistent from the point of view of each base chain (but different base chains may "perceive" different extensions). This allows us to, for example, move objects to base chains even after the chimera chain loses atomic guarantees.

## Kill Chains

Likewise, it's probably useful to kill chimera chains no one is using anymore. If we don't kill them, when quorums change all of chimera chains need to get an update, and that can become infeasible. One possibility is to allow chains with no objects on them (everything has moved out) to execute a special "kill" transaction that prohibits any future transactions, and sends an IBC message to all parent chains. On receipt, parent chains could remove that chimera chain from their registry.

## Protocol Description

This section describes how a chimera block is appended to the existing chimera chain assuming all the setup has taken place.

For simplicity, this protocol is written as if we're deciding on one thing: the specific block that belongs on a specific blockchain at a specific height. All state and references are specific to this blockchain / height pair. We do not care about messages before this height. This height may be defined using the last finalized block in the blockchain.

### Learner Graph

For each learner $\red{a}$, we call its set of quorums $\red{Q_a}$.

For each pair of learners $\red{a}$ and $\blue{b}$, there are a specific set of conditions under which they require agreement. We enumerate these as $\edge{\red{a}}{\blue{b}}$, a set of "safe sets" of acceptors: whenever at least one set in $\edge{\red{a}}{\blue{b}}$ is composed entirely of safe (non-byzantine, but possibly crashed) acceptors, $\red{a}$ and $\blue{b}$ must not decide different things.

We designate the set of acceptors who are actually safe $\reallysafe$. This is of course determined at runtime, and unknown to anyone.

### Messages

The protocol is carried out by sending and receiving messsages. The table below describes the structure of a typical heteregenous paxos message.

| Field    | Type     | Description |
| -------- | -------- | ----------- |
| chainId  | `Id`       | Identifies this Chimera Chain |
| height   | `uint64`   | Current height of the chimera chain |
| pktType  | `enum PktType {1A, 1B, 2A}` ||
| ballot   | `Ballot` = `(Timestamp, Hash)`    | This consists of the hash of the proposed block and the timestamp of the initiated ballot. There is a total lexicographical order on `Ballot`.|
| learner  | `Id`       ||
| sig      | `Sig`      | The signature field `sig` unforgeably identifying its sender, e.g., the message is signed, and the sender has a known PK in some PKI.|
| refs     | `Vec<Hash>` | The list of hashes of messages received previously. |

In general, acceptor relay all sent or received messages to all learners and other acceptors. This ensures that any message received by a real acceptor is received by all real acceptors and learners.

#### Definition: Message Signer

$$
  \sig{\green x : Message} \triangleq
  \textrm{the acceptor or proposer that signed }\green x
$$

#### Definition: Message Set Signers

We can define $\sig{}$ over sets of messages, to mean the set of signers of those messages:
$$
  \sig{\green s : set(Message)}
  \triangleq \cb{\tallpipe{\sig{\blue m}}{\blue m \in \green s}}
$$

Messages also contain a field `refs`, which includes chained hashes of every message the sender has sent or received since (and including) the last message it sent. As a result, we can define the transitive references of a message, which should include every message the sender has ever sent or received:

#### Definition: Transitive References

$$
  \tran{\green x}
  \triangleq
    \cb{\green x}
  \cup
    \bigcup_{\blue m \in \green{x.\mathit{refs}}} \tran{\blue m}
$$

To ensure that acceptors and learners _fully understand_ each message they receive, they delay doing any computation on it (sometimes called delivery) until they have received all the messages in `refs`. As a result, acceptors and learners will always process messages from any given sender in the order they were sent, but also from any messages that sender received, and recursively.

<!-- ### Protocol Description

1. **Propose a block**: A proposer proposes a new block that the acceptor will vote on by sending a message containing the hash of the proposed block along with a time stamp of the ballot initiation. This message is called _1a-message_. If there is an existing chimera chain the proposer can built upon that chain and if the proposer is starting a new chimera chain it needs to lock some funds for that.

<!-- The block consists of transactions from both chains or just on of the chains. The transaction can be bundled together to make sure they are carried out atomically.

more than one block be finalized like in Grandpa? and decoupling block prduction from finalization
    - In principle, yes. Heterogeneous Paxos would serve the roll of a "finality gadget" in Grandpa's terms, but blocks could be produced at any rate

-->

### **Consensus Round: Ballot**

Next, we briefly describe how the communication for a consensus round works. Consensus is reached in four steps: proposing the chimera block, acknowledging receipt of proposals,  establishing consensus, and termination.

Suppose we have two learners $l_1$ and $l_2$ from two different blockchains.

#### **$1a$ message: proposing blocks**

<!--To propose a chimera block, proposers send $1a$ messages, each carrying a value (the atomic transaction for example) and unique ballot number (round identifier), to all acceptors. -->

A proposer proposes a new block by sending a $1a$ message to all acceptors,
which includes

- a value (the atomic transaction for example)

- a unique ballot number (round identifier)

- a message containing the hash of the proposed block along with a time stamp of
  the ballot initiation.

If there is an existing chimera chain, the proposer can built upon that chain
and if the proposer is starting a new chimera chain it needs to lock some funds
for that.

Also, the acceptor needs to check validity as soon as possible: don't even
"receive" an invalid proposal (or at least don't send a "1b" message in
response).

#### **$1b$ message: acknowledging receiving proposals**

On receipt of a $1a$ message, an acceptor sends an ackowledgement of its receipt
to all other acceptors and learners in the form of $1b$ message.

#### **$2a$ message: establishing consensus**

When an acceptor receives a $1b$ message for the highest ballot number it has
seen from a learner $l_1$’s quorum of acceptors, it sends a $2a$ message labeled
with $l_1$ and that ballot number.

There is one exception: once a safe acceptor sends a $2a$ message $m$ for a
learner $l_1$, it never sends a $2a$ message with a different value for a
learner $l_2$, unless one of the following is true:

* It knows that a quorum of acceptors has seen $2a$ messages with learner $l_1$
  and ballot number higher than $m$.

* It has seen Byzantine behavior that proves $l_1$ and $l_2$ do not have to
  agree.

##### Specifics of establishing Consensus

In order to make a learner decide, we need to show that another, _Entangled_
learner could not already have decided.

##### Definition: Entangled

In an execution, two learners are _entangled_ if their failure assumptions
matched the failures that actually happen:

$$
\entangled{\red a}{\blue b} \triangleq \reallysafe \in \edge{\red a}{\blue b}
$$

If some learner $l_1$ does not agree with some other learner $l_3$, then learner
$l_2$ cannot possibly agree with both $l_1$ and $l_3$.

##### Definition: Heterogeneous Agreement

* Within an execution, two learners have _agreement_ if all decisions for either learner have the same value.
* A heterogeneous consensus protocol has _agreement_ if, for all possible executions of that protocol, all entangled pairs of learners have agreement.

##### Definition: Accurate Learner

An _accurate_ learner is [entangled](#definition-entangled) with itself:

$$
\accurate{\red a} \triangleq \entangled{\red a}{\red a}
$$

A learner whose quorums contain too many failures is inaccurate. This is the
equivalent of a chain that can fork.

In order to prevent entangled disagreement, we must define the conditions that
will ultimately make learners decide:

##### Definition: Get1a

It is useful to refer to the $1a$ that started the ballot of a message: the
highest ballot number $1a$ in its transitive references.

$$
\geta{\green x} \triangleq
\argmax_{\blue m:\textit{1a}\in\tran{\green x}}{\blue{m.ballot}}
$$

##### Definition: Ballot Numbers

The ballot number of a $1a$ is part of the message, and the ballot number of
anything else is the highest ballot number among the $1a$s it (transitively)
references.

$$
  \ba{\green x} \triangleq \geta{\green x}.ballot
$$

##### Definition: Value of a Message

The value of a $1a$ is part of the message, and the value of anything else is
the value of the highest ballot $1a$  among the messages it (transitively)
  references. $$ \va{\green x} \triangleq \geta{\green x}.value $$

#### **Terminate: Finalizing blocks**

A learner $l_1$ decides when it receives $2a$ messages with the same ballot
number from one of its quorums of acceptors.

If no decision can be reached within a certain time, proposers must begin a new
round (with a higher timestamp, and thus a higher Ballot). Proposers can start a
new round by proposing a new block or by trying to finalize the same block again
(in case there was no consensus).

##### Definition: Decision

A learner decides when it has observed a set of $2a$ messages with the same
ballot, sent by a quorum of acceptors. This will allow the learner to _decide_
on the value of the $2a$ messages in the set. We call such a set a _decision_:


$$ \decision{\red a}{\red{q_a}} \triangleq \sig{\red{q_a}} \in \red{Q_a}
  \ \land\
  \forall \cb{\green x,\blue y} \subseteq \red{q_a} . \ \p{\andlinesThree
    {\ba{\green x}=\ba{\blue y}}
    {\green{x.lrn}=\red a}
    {\green x:\textit{2a}}}
$$

Now we are ready to discuss what makes a _Well-Formed_ $2a$ message. This
requires considering whether two learners might be entangled, and (unless we can
prove they are not engangled), whether one of them might have already decided:

##### Definition: Caught

Some behavior can create proof that an acceptor is Byzantine. Unlike Byzantine
Paxos, our acceptors and learners must adapt to Byzantine behavior.  We say that
an acceptor $\purple p$ is _Caught_ in a message $\green x$ if the transitive
references of the messages include evidence such as two messages, $\red m$ and
$\blue{m^\prime}$, both signed by $\purple p$, in which neither is featured in
the other's transitive references (safe acceptors transitively reference all
prior messages).

$$
  \caught{\green x} \triangleq
  \cb{\tallpipe{\sig{\red m}}{\andlinesFour
        { \cb{\red m, \blue{ m^\prime}} \subseteq \tran{\green x} }
        {  \sig{\red m} = \sig{\blue{ m^\prime}}}
        { \red m \not\in \tran{\blue{m^\prime}}}
        { \blue{m^\prime} \not\in \tran{\red m}}
   }}
$$

**Slashing**: Caught proofs can be used for slashing.

##### Definition: Connected

When some acceptors are proved Byzantine, clearly some learners need not agree, meaning that $\reallysafe$ isn't in the edge between them in the CLG: at least one acceptor in each safe set in the edge is proven Byzantine. Homogeneous learners are always connected unless there are so many failures no consensus is required.
$$
  \con{\red a}{\green x} \triangleq
  \cb{\tallpipe{\blue b}{\andlinesTwo
        {\purple s \in \edge{\red a }{ \blue b} \in \clg}
        {\purple s \cap \caught{\green x} = \emptyset }
      }
     }
$$

##### Definition: Buried

A $2a$ message can become irrelevant if, after a time, an entire quorum of
acceptors has seen $2a$s with different values, <span style="background-color:
#E2E2FF">the same learner</span>, and higher ballot numbers. We call such a $2a$
_buried_ (in the context of some later message $\purple y$):

$$
  \buried{\green x : \textit{2a}}{ \purple y} \triangleq
  \cb{\tallpipe{\sig{\red m}}{\andlinesSix
      {\red m \in \tran{\purple y}}
      {\blue z : \textit{2a}}
      {\cb{\green x, \blue z} \subseteq \tran{\red m}}
      {\va{\blue z} \ne \va{\green x}}
      {\ba{\blue z} > \ba{\green x}}
      {\hetdiff{\blue{z.lrn} = \green{x.lrn}}}
  }}
  \in \green{Q_{\hetdiff{x.lrn}}}
$$

##### Definition: Connected 2a Messages

Entangled learners must agree, but learners that are not connected are not
entangled, so they need not agree. Intuitively, a $1b$ message references a $2a$
message to demonstrate that some learner may have decided some value. For
learner $\red a$, it can be useful to find the set of $2a$ messages from the
same sender as a message ${\green x}$ (and sent earlier) which are still
[unburied](#definition-buried) and for learners connected to $\red a$. The $1b$
cannot be used to make any new $2a$ messages for learner $\red a$ that have
values different from these $2a$ messages.

$$
      \cona{\hetdiff{\red a}}{\green x} \triangleq
      \cb{\tallpipe{\blue m}{\andlinesFive
          {\blue m : \textit{2a}}
          {\blue m \in \tran{\green{x}}}
          {\sig{\blue m} = \sig{\green x}}
          {\lnot \buried{\blue m}{\green x}}
          {\hetdiff{\blue{m.lrn} \in \con{\red a}{\green x}}}
      }}
$$

##### Definition: Fresh

Acceptors send a $1b$ message whenever they receive a $1a$ message with a ballot number higher than they have yet seen. However, this does not mean that the $1b$'s value (which is the same as the $1a$'s) agrees with that of $2a$ messages the acceptor has already sent. We call a $1b$ message _fresh_ (with respect to a learner)  when its value agrees with that of unburied $2a$ messages the acceptor has sent.
$$
    \fresh{\hetdiff{\red a}}{\green x : \textit{1b}} \triangleq
    \forall \blue m \in \cona{\hetdiff{\red a}}{\green x} . \
      \va{\green x} = \va{\blue m}
$$

##### Definition: Quorums in Messages

$2a$ messages reference _quorums of messages_ with the same  value and ballot. A $2a$'s quorums are formed from [fresh](#definition-fresh) $1b$ messages with the same ballot and value.
$$
  \qa{\green x : \textit{2a}} \triangleq \cb{\tallpipe{\red m}{\andlinesFour
  {\red m : \textit{1b}}
  {\fresh{\hetdiff{\green{x.lrn}}}{\red m}}
  {\red m \in \tran{\green x}}
  {\ba{\red m} = \ba{\green x}}
}}
$$

##### Definition: Well-Formed

We define what it means for a message to be _well-formed_.

$$
  \begin{array}{l}
WellFormed(\purple u : \textit{1a}) \triangleq
  \ {\purple u}.\mathit{refs} = \emptyset
\\
WellFormed(\green x : \textit{1b}) \triangleq
  \ {\green x}.\mathit{refs} \ne \emptyset
  \ \land\ \forall\,\blue y \in \tran{\green x} .
  \ \green x \ne \blue y
  \ \land\ \blue y \ne \geta{\green x}
  \ \Rightarrow\ \ba{\blue y} \ne \ba{\green x}
\\
WellFormed(\red z : \textit{2a}) \triangleq
  \ {\red z}.\mathit{refs} \ne \emptyset
  \ \land\ \sig{\qa{\red z}} \in \red{Q_{\hetdiff{z.lrn}}}
\end{array}
$$

An acceptor who has received a $1b$ sends a $2a$ for every learner for which it
can produce a Well-formed $2a$.

Before processing a received message, acceptors and learners check if the
message is well-formed. Non-wellformed messages are rejected.

### Incentive Model

Goal:

* Incentivizing token holders to put down their stake for security

* Disincentivizing byzantine behavior

Rewards:

* Participating in consensus based on backing stake: this includes validating and voting

* Producing blocks

Slashing: there are a number of offenses

* Invalid blocks

* Equivocation (caught)

### Fees

!!! quote

     The first question is once there is no demand for atomic batches of transactions, do we keep the chimera chain alive?

We need to figure out whether killing the chimera chain (and potentially
requiring a new genesis later) is not too expensive.

!!! quote

     The second question is whether we update the quroum changes whenever they happen or when we have a transaction?

The first option is expensive and can lead to attack if not handled well. We
need to figure out whether the latter option is safe.

* If the answer is yes for first question and we pick the first option for the
  second question:

Since all chimera chains need to be updated when the quorums on the base chains
change, we need to figure out who pays for these updates. For example, a chimera
chain might have had a block produced last week, but since the has been updated
200 times that is 200 blocks that do not have any transactions with transaction
fees. If this is not paid by anyone, it becomes a burden for acceptors and an
attack vector for the adversary.

We may need to add a "locked" fee for making new chimera chains. In particular,
we don't want an attacker to make a lot of chains, forcing base chains to update
all of them with each quorum change.

Alternatively, each "chimera chain" could keep an account on each base chain
that is funded by a portion of transaction fees, from which a small fee is
extracted with each validator update. When the account runs dry, the
(parent)base chains are allowed to kill the chimera chain (even if there are
still objects on there). We could allow anyone to contribute to these accounts.
We could even prohibit anyone who did not contribute from sending IBC messages
between chimera and parent chains.

## Security Discussion

Note that the chimera cannot guarantee atomicty under the same adversary
assumption as the base chains. For example, if we assume the adversary to
control less than 1/3 of the stake to assure safety on the base chains,
atomicity is not guaranteed for such an adversary but only a weaker one. This is
important for users so they can decide whether for their transaction chimera
chians would be secure enough.

By setting the quorums of each learner to be the same as the quorums of the
corresponding base chain, we ensure that each learner's view is *as consistent*
as the base chain. Specifically, two instantiations of the learner for some base
chain $A$ should decide on the same blocks in any chimera chain, unless the
adversary is powerful enough to fork chain $A$.

"Accurate" (or "self-engangled") learners (defined above) correspond to base
chains where the adversary is in fact powerful enough to fork the chain. Proving
that a learner is accurate is equivalent to proving that its base chain cannot
fork.

Two learners $\red{a}$ and $\blue{b}$ corresponding to different base chains
will decide on the same blocks (which is what makes atomic batches useful), so
long as one of the safe sets in $\edge{\red{a}}{\blue{b}}$ is composed entirely
of safe acceptors. The stake backing these safe sets represents the "assurance"
that atomic batches remain atomic, as well as the maximum slashing punishment
should they lose atomicity.

Loss of atomicity is a bit like a "trusted bridge" that turns out not to be
trustworthy: each state machine within the chimera chain has as much integrity
as its base chain, but atomicity properties of multi-state-machine atomic
batches have a lesser, but still well-defined, guarantee. Loss of atomicty
allows double spending on the chimera chain. And while misbehavior has happened
in such an attack it is not trivial to slash the misbehaving acceptor since
according to each chain everything has been carried out correctly.

## Open Challenges

### Programming Model

#### Atomic Batches

We'll need a way to specify that a batch of transactions should be committed
together or not at all. Ideally, this should communicate to the programmer how
reliably this atomicity is (see "practical considerations" below). On an chimera
chain, batches can include transactions from any of their "main chains". If we
want to have match-making, transactions will need to be able to say something
like "if I'm in an atomic batch that matches these criteria, then do this...".

Each atomic batch should be scheduled within one block.

(We encode transactions with Portobuff and Borsht.) We need define structures
such that transactions can be bundled and cannot be carried out separately.

#### Atomic Communication

Transactions within an atomic batch need to be able to send information to each
other (and back). For example, in a market with a fluctuating exchange rate, a
market transaction could send a message to an account, which transfers money,
and sends a message to another account, which transfers goods. We need a
language in which this communication takes place with minimal constraints on the
state machines involved, so we should probably adapt the IBC communication
language.

We need to figure out inter-chain communication works for transactions
communicating with each other within an atomic batch.

#### Can we have synchronous (in terms of blocks) IBC?

Yes: when the quorums involved in two chains are the same, then we can guarantee
that (unless there are sufficient failures to fork the chain) an IBC message
sent in one chain will arrive at the other chain (in a transaction) within a
specific number (perhaps as few as 1?) of blocks. This is because some of the
machines in the quorum that approved the "send" transaction must be in the
quorum that decides the next block, so they can refuse to decide on blocks that
lack the "receive" transaction.

Note that we may need to rate-limit sends to ensure that all sends can be
received in time (availability).

Note also that blinding transactions makes this hard.

### Match Making

We can in priciple do cross-chain match-making. If we want an on-chain market,
an chimera chain might be a good place to do it. However, full nodes in the
gossip layer might be able to gather sets of transactions that match the
transactions' "If I'm in an atomic batch ..." criteria, bundle them into atomic
batches, and then send those off to be committed.

We may want to incorporate some incentive scheme for good match-making.
Matchmakers include nodes who are full nodes on both chains, and in principle
could include any node who sees the request transactions.

### Changing Quorums?

<!--Assume we have one "main chain" that decides who the quorums used by some other (possibly heterogeneous) chains are. Hopefully, quorum changes are infrequent. -->

#### 2 Phase Commit

We could require that any quorum-chainging transaction has to be 2-phase
committed. Essentially, the "main chain" announces that it won't progress beyond
a certain block until everyone has appended a new block that sets the (same) new
quorums, and sends a response by IBC. It can then progress only with IBC
responses from all the other chains that use these quorums.

<!--This solution is potentially slow: arbitrarily many chains may have to be involved. That said, at least in principle, they all have the same safety and liveness properties.-->

#### Synchronous IBC

We may be able to leverage our "synchronous" IBC idea above for faster quorum
changes. The difficulty is that it allows a finite number of blocks to be
appended to the chimera chains before they receive the quorum change method.
These chains can be arbitrarily slow, so that could take arbitrarily long.

Need to figure out inter-machine communication for acceptors, since they might
run many machines.

---

## Discussion Questions /Practical Considerations

* Optimizing messgaing: Pipelining (from Hotstuff), Kauri, BFTree

* Replicating state machines

* Probems Tendermint has:

    * Doesnt allow many validators

    * Lightclient design

* Optimizing recoveryfrom slow finalization: Separating block prosuction from finalizing, finalzing more than one block

* ABCI ++? Another version of it

* Look into other papers of Dalia Malkhi / Fast HotStuff?


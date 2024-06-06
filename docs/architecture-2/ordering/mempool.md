---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---
# Mempool

## Summary

Validator nodes run the mempool protocol.
They receive transaction candidates from clients, <!-- TODO: user / client/ ... ⁈ -->
store them, 
and make them available for the [[Execution Engines|execution engine]] to read.
The mempool protocol,
which is based on [Narwhal](https://arxiv.org/abs/2105.11827) also produces
a [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of _vertices_,<!--
TODO: change to vertices? -->[^1]
which reference batches of transaction candidates (via hash), 
and prove that those transaction candidates are available for 
the [[Execution Engines|execution engine]].
These vertices (or hashes of them) are what validators propose as values in the [[Consensus|consensus protocol]],
in order to establish a total order of transaction candidates.

[^1]: We are close in terminology to Bullshark<!-- citation needed-->,
concerning the mempool ᴅᴀɢ.


## Narwhal + predecessor links

While keeping true to the "spirit"  of the original Narwhal protocol,
the mempool protocol is incorporating 
one additional type of edge[^2] in the mempool ᴅᴀɢ:

[^2]: The additional edge will become relevant for the heterogeneous setting.

>Whenever a validator's Narwhal primary produces a vertex,
>it must reference in that vertex not only 
>a quorum of vertices from the previous round, but<!-- TODO change 'round' to '?'--> 
>also the most recent vertex that was produced by that validator.

Moreover, 
we distinguish between certificates of availability and integrity.

### Overview

Each validator node has

- one *primary* engine and
- many *worker* engines.

A client 
must choose one or several specific worker engine on one or several validator nodes
as destination <!-- "target" in actor speak-->for each transaction candidate ordering request.

#### Workers

Worker enginees ensure transaction candidates are available.
Transaction candidates are batched.
Each batch is erasure-coded (possibly simply copied) across 
a *weak quorum* of workers;
note that 
only signed hashes of those batches are sent to primaries.
The rationale is that, in this way,
the high-bandwidth work of replicating transaction candidates 
is done by workers instead of primaries,
avoiding the "leader bottleneck" <!-- citation needed 
-->such that consensus decisions are faster and/or cheaper.

#### Primaries 

Primary engines establish a partial order of transaction candidate vertices
(and by extension transaction candidates), in the form of a structured DAG.
The DAG proceeds in *rounds*:
each primary produces at most one vertex in each round.
That vertex references vertices from prior rounds.

Primaries assemble vertices (both their own and for other primaries) from collections of worker hashes, and references to prior vertices.
They then sign votes, stating that they will not vote for conflicting vertices, and (optionally) that their workers have indeed stored the referenced transaction candidates.
Primaries collect votes concerning their own vertices, producing vertices: aggregated signatures showing a vertex is unique.

More formally, we present the Heterogeneous Narwhal protocol as the composition of two crucial pieces: the Heterogeneous Narwhal Availability protocol, and the Heterogeneous Narwhal Integrity protocol.

<!--

### Vocabulary

- *Learner*s dictate trust decisions: just like in Heterogeneous Paxos, we use a Learner Graph. In diagrams, we usually represent learners with colors (red and blue).
- <img src="quorum.svg" alt="quorum" height="12pt"/> *Quorum*: a set of validators sufficient for a Learner to make vertices. Each Learner has a set of quorums.
- *Intact Learner*: any 2 quorums for an Intact Learner have a correct validator in their intersection. Most of our guarantees apply only to Intact Learners.
- *Entangled Learners*: a pair of learners *A* and *B* are entangled if, for any quorum *Qa* of *A*, and any quorum *Qb* of *B*, the intersection of *Qa* and *Qb* contains a correct validator.
Some guarantees apply pairwise to Entangled Learners: they are, in a sense, guaranteed to agree on stuff.
- <img src="weak_quorum.svg" alt="weak quorum" height="12pt"/> *Weak Quorum*: a set of validators that intersects every quorum. Weak Quorums are Learner-specific, so when we say *weak quorum for every learner* we mean a set of validators that intersects every quorum of every Learner.
- <img src="transaction.svg" alt="transaction" height="12pt"/> *Transaction*: data from clients to be ordered. We do not specify how it's formatted.
- *Batch*: a set of transactions collected by a Worker.
- <img src="erasure_share.svg" alt="erasure share" height="12pt"/> *Erasure Share*: data transmitted to a weak quorum of listening workers, such that any Quorum of validators can re-construct the original data (Transaction or Batch of Transactions).
- <img src="worker_hash.svg" alt="worker hash" height="12pt"/> *Worker Hash*: a signed digest of a batch of transactions collected by (and signed) by a worker.
- <img src="header.svg" alt="header" height="12pt"/> *Header*s have:
  - an associated Primary (who "created" this header)
  - a set of Worker Hashes (from workers on the same validator as this primary)
  - an Availability Certificate for the previous Vertex issued by this primary
  - at most one Signed Quorum for each Learner
- <img src="availability_certificate.svg" alt="availability certificate" height="12pt"/> *Availability Certificate*: an aggregation of signatures from a Weak Quorum attesting that everything referenced by a particular Vertex is available. Must include a signature from the Vertex's primary.
- <img src="block.svg" alt="block" height="12pt"/> *Block*: an aggregation of Vertex signatures from a quorum of a specific learner attesting that they will not attest to any conflicting vertex. Also includes an Availability Certificate. Should include all signatures a primary has gathered for that vertex at the time (signatures in the Availability Certificate count).
- <img src="signed_quorum.svg" alt="signed quorum" height="12pt"/> *Signed Quorum*: a quorum of vertices with the same learner and round, signed by a primary. These are referenced in vertices.

![Data Structure](data_structure.svg)

## Heterogeneous Narwhal Availability Protocol

![Availability Protocol Time-Space Diagram](workers.svg)
(note the giant curly-brace represents a Weak Quorum of validators)

### Batches and Worker Hashes

When a worker has collected a batch of transactions, it transmits erasure shares (possibly full copies) of those transactions to other workers on a *weak quorum for every learner* of validators.
What's important about this erasure coding is that any Quorum of any Learner can reconstruct every transaction.
Furthermore, workers must be able to verify that they are in fact storing the correct Erasure Share of the data referenced in the Worker Hash.
One way to accomplish this is to transmit a complete copy of all the data to an entire Weak Quorum for every Learner.

In fact, rather than wait until a batch is complete to start transmitting, workers can stream erasure shares as they receive transactions.
When it has completed a batch, a worker also transmits a signed *Worker Hash* to those other workers, and its own primary.
We do not specify when workers should complete batches, but perhaps it should be after some timeout, or perhaps primaries should signal workers to complete batches. Batches should not be empty.

### Signed Quorums and Vertices

Primaries ultimately produce vertices for each round, for each Learner, and send those vertices to other Primaries.
When a primary for validator `V` has received vertices for learner `L` and round `R` from an entire quorum of validators for learner `L`, it signs that collection, producing a *Signed Quorum* object, which identifies the validator `V`, the learner `L`, and the round `R`.
The Signed Quorum is then broadcast (or erasure coded) to primaries on a *weak quorum for every learner* of validators.
Much like batches, it is important that any Quorum for any Learner can re-construct the entire Signed Quorum.

Periodically, each primary `P` produces *Vertices*.
Each Vertex contains:

- a set of signed Worker Hashes, all signed by `P`'s validator
- a hash referencing at most one Signed Quorum per Learner, all signed  by `P`
- an *Availability Certificate* (we'll get to how those are made shortly) for the previous Vertex `P` issued.
Vertices should be relatively small.
Each primary then sends the vertex to all the other primaries.

When a Primary receives a Vertex, it can produce an *Availability Vote* (which is a digital signature) iff
- the primary has stored its share of all Signed Quorums referenced,
- the primary has received messages from its workers indicating that they have stored their shares of all the Batches referenced
The Availability Votes are then transmitted to the Vertex's Primary.

When a primary receives Availability Votes for a Vertex from a weak quorum for every learner, it can aggregate those signatures to produce an *Availability Certificate*, which proves that the Vertex (and its contents) are available to any Quorum.
Availability Certificates should be small.
Note that, if primaries broadcast Availability Certificates as soon as they produce them, other primaries may have all the components necessary to "receive" a Vertex even before the Vertex's Primary actually sends it.
Specifically, they may have:

- Signed Batch Vertices from their listening Workers
- Signed Quorum shares received earlier from the Primary
- Availability Certificate received earlier from the Primary

## Heterogeneous Narwhal Integrity Protocol

So far, only Signed Quorums have been Learner-specific: everything else requires a weak quorum for every learner.
However, in the Integrity Protocol, almost everything is Learner-specific.
Furthermore, Workers are not involved in the Integrity Protocol: only Primaries.
![Integrity Protocol Time-Space Diagram](primaries.svg)
Each Vertex `H` features a predecessor `H'`: the availability certificate in `H` references the vertex `H'`.
When a Primary receives a Vertex `H`, it can produce an *Integrity Vote* iff it has not produced an Integrity vote for any other Vertex with the same predecessor as `H`
In essence, this means that each correct Primary signs, for each other (even incorrect) Primary, a unique chain of Vertices.
This will ensure that no primary can produce conflicting vertices for entangled Learners.
Integrity Votes are transmitted back to the Primary associated with the Vertex.
In practice, a Integrity and Availability votes may be combined for Primaries who can cast both.

For each Vertex it produces, a Primary can calculate its *Learner Vector*: this represents, for each Learner, the highest round number of any quorum referenced in this Vertex or its ancestors (its predecessor, of its predecessor's predecessor, etc.).
If, for some Learner `L`, a vertex `H` has a greater round number `R` in its *Learner Vector* for `L` than did `H`'s predecessor, then the Primary can produce a *Block* for learner `R` and round `L`.
Intuitively, a Primary produces a block whenever it gets a quorum for a Learner in a latest round.

A block for learner `L` includes an Availability Certificate, as well as an aggregated signature formed from the Integrity Votes of (at least) a quorum (for learner `L`) for the same Vertex.
Vertices are transmitted to all other Primaries, who use them to form Signed Quorums.

If a Primary uses the same Vertex to make vertices for multiple Learners, each block it produces must use a superset of signatures as the previous. This ensures that if the Primary produces a block for Learner A and then a block for learner B, the Block for learner B effectively includes the block for learner A.
We can use this when we later establish a total ordering: any reference to the learner B block also effectively references the learner A block.

Here is an example timeline of a Primary producing vertices, availability certificates, and vertices.
Vertices are color coded by learner and include a round number.
Vertices display *Learner Vectors*.
![Single Primary Timeline](primary_timeline.svg)

## DAG Properties

Independently, the vertices for each Learner form a DAG with the same properties as in the original Narwhal:
![Blue DAG](quorums_blue_5_red_0.svg)
(In these diagrams, vertices reference prior vertices from the same Primary; I just didn't draw those arrows)

Note that vertices reference a quorum of vertices from the previous round.
This does not require that the same primary produced a block for the previous round.
In round 5, Primary 3 can produce a block if it has received a quorum of round 4 vertices from other Primaries.

Of course, primaries do not necessarily produce vertices for the same round at the same literal time.
Here we see primaries producing vertices for round 3 for red learner at different times, depending on when they finish batches, or receive a round 2 quorum, or enough votes:
![Blue DAG](quorums_blue_0_red_3.svg)
In Heterogeneous Narwhal, these two DAGs are being created simultaneously (using the same sequence of Vertices from each Primary, and many of the same Votes):
![Blue and Red DAG](quorums_blue_5_red_3.svg)
Note that round numbers for different learners do not have to be close to each other.
Red round 3 vertices are produced after blue round 5 vertices, and that's ok.

Furthermore, rounds of different learners are not totally ordered.
Red round 3 cannot really be said to happen before, or after, blue round 4.

### Fair Broadcast

In Homogeneous Narwhal, any block which is referenced by a weak quorum in the following round will be (transitively) referenced by all vertices thereafter. Heterogeneous Narwhal has analogous guarantees:

#### Any block for learner `A`  referenced by a weak quorum for learner `A` will, after 3 rounds, be (transitively) referenced by all future vertices of learners entangled with `A`.

Specifically, such a block `B` in round `R`, will be (transitively) referenced by all `A`-vertices in round `R+2`.

Consider the first round for learner `B` using at least a quorum of vertices either used in `A` round `R+2` or after their primaries' vertices for `A` round `R+2`.
Given that Learner `B` is entangled with `A`, any `B`-quorum for this round will be a descendant of an `A`-block from round `R+2`, and therefore, of `B`.

## Consensus

![Leader Path](leader_path_3.svg)

In order to establish a total order of transactions, we use [Heterogeneous Paxos](consensus-v1.md#consensus) to decide on an ever-growing path through the DAG (for each Learner).
Heterogeneous Paxos guarantees that, if two Learners are *entangled*, they will decide on the same path.
In order to guarantee liveness (and fairness) for each Learner's transactions, we require that:

*For any accurate learner `L`, if one of `L`'s quorums remains live, and an entire quorum of `L` issues vertices for round `R`, consensus will eventually append one of `L`'s round-`R` vertices, or one of its descendants, to `L`'s path.*

Crucially, if two learners are not entangled, and their vertices never reference each other, consensus should not forever choose vertices exclusively from one learner.
This does require a minimal amount of fairness from consensus itself: as long as vertices for learner `L` keep getting proposed (indefinitely), consensus should eventually append one of them to the path.

### Choosing a total order

Given a consensus-defined path, we can impose a total order on all transactions which are ancestors of any block in the path.
We require only that, given some block `B` in the path, all transactions which are ancestors of `B` are ordered before all transactions which are not ancestors of `B`.
Among the transactiosn which are ancestors of `B` but not of its predecessor in the path, total order can be imposed by some arbitrary deterministic function.


-->


<!--
# Mempool

The mempool receives transaction requests
and stores them such that they are available for the
[[Execution Engines|execution engines]].
The mempool triggers the execution of transaction candidates
for all transaction candidates received by any validator.
Finally,
it also provides partial ordering information to shards,
and contributes to
the dissemination of future lock requests to the state.
In V1,
the mempool is roughly a FIFO queue that takes
transaction requests and passes them on to execution.

## Components

- [[Worker Engine|Workers]] receive
  transaction requests from users or solvers and
  keep transaction data available for executors,
  which they spawn for the purpose of executing transactions
  (in cooperation with shards).
  After successful execution,
  workers keep execution logs available.[^100]

- [[Execution Supervisor]]s are the engines that are in charge
  of spawning new executor processes that workers then use
  to execute transaction requests.

[^100]: In V2, this will be only for a limited period of time.


---

**TODO** 
1. **TODO**  find old  version s (main / v2 / v1 ) of this page
2. **TODO**  conglomerated them and take care of execution !!! 

---

-->

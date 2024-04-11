---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Ordering and Execution Engines

The ordering and execution engines receive transaction requests from users,
order the transaction requests, and
finally execute them.
- The [[Mempool Engines|mempool engines]] are responsible for
  storing transaction data and linking them suitably into
  a “global” directed acyclic graph of vertices,
  each of which references the submitted transactions (via [[WorkerHash|worker hashes]]).
- The [[Consensus Engine|consensus engine]] is responsible for choosing anchor blocks
  in collaboration with the mempool engines.
- The [[Execution Engines|execution engines]] execute the transactions
  and take care of maintaining the global state of the chain.

## The transaction: from request to execution

Consider the “life cycle” of a transparent asset transfer $T$.
We will go through all the messages exchanged between
 [[Mempool Engines|mempool]], [[Consensus Engine|consensus]], and
 [[Execution Engines|execution engines]], starting from the initial
 user request until the execution of the transfer is stored on chain.

- First, user $U$ sends a [[TransactionRequest|transaction request]]
   $R_T$ to a [[Worker Engine|worker]] $W$.
  In principle, $U$ can choose any worker:
   either they have a preference for a specific worker
   (e.g. because they have a business relationship)
   or the user's wallet has chosen a suitable worker.
  The user could be a [[Solver]] that is also operating a validator
   and thus likely will choose one of its own workers.
  <!-- Here we of course have already the example that
  workers might have some kind of priority service... -->

### Mempool

- The [[Worker Engine|worker]] $W$ then
   sends copies of this transaction request $R_T$ to
   all its mirror workers $W_1, \dotsc, W_n$ such that
   all correct validators (eventually) become aware of the
   [[NewTransaction|new transaction]].
  Transaction copies are stored such that other nodes can retrieve
   them if they need to.
  The [[Worker Engine|worker]] also
   [[ExecuteTransaction|sends the transaction]] to its validator's
   [[Executor Engine|execution engine, starting a new executor process]].

- Worker $W$ will eventually complete a batch of transactions $B$
   (after  receiving a number of additional transactions);
   a _batch_ is simply a list of transactions.
  The worker $W$ numbers batches consecutively with natural numbers
  such that the transaction request $R_T$ will be _stamped_ with a unique pair:
   a batch number $n_B$,
   and a sequence number $s_{R_T}$ within batch $B$.
  (In fact, the triple $(W,n_b,s_{R_T)}$ is the _transaction fingerprint_ of $T$.)
  After closing batch $B$, worker $W$:
  - informs its primary $P$ (another engine within the same validator) of the
    [[NewWorkerHash|new worker hash]] $H_B$ for the batch $B$
    (this will be included in a vertex of the [mempool ᴅᴀɢ](#certificates-and-the-mempool-dag)),
    and
  - messages all mirror workers,
    notifying them of the [[WorkerHashFingerprint|fingerprint of the new worker hash]]
    (such that they can also make their primaries aware of the worker hash $H_B$).

- The primary $P$ eventually creates a new vertex $X$
  (including additional worker hashes from other workers on the same validator).
  The vertex contains of a list of worker hashes $H_{B_1}$, …, $H_{B_k}$.
  At genesis, the vertex is just a list of worker hashes with the
   [[Identity|ɪᴅ]] of the primary. <!--
  Thereafter, vertices also contain an [[AvailabilityCertificate]] for
   the previous vertex $P$ issued.
  -->(Typically, further data is required to form a vertex of the mempool ᴅᴀɢ,
  which we describe after all “data types” have arisen at their natural spot).
  The primary announces the new vertex $X$ by broadcasting the
   [[HeaderAnnouncement|new vertex fingerprint]] to all primaries.
  The primary then sends
   [[TimestampOrderingInformation|transaction ordering information]]
   about transactions referenced in $X$ to all of its validator's
   [[Execution Engines|execution engine's]] [[Shard Engine|shards]].

- Workers on other validators will receive all relevant transactions for vertex $X$.
  For each transaction referenced by $X$'s worker hashes, workers
   store a copy.
  These [[Worker Engine|workers]] also
   [[ExecuteTransaction|send the transaction]] to their validator's
   [[Executor Engine|execution engine, starting a new executor process]].
  When a worker has stored copies of an entire batch, it sends a
   [[WorkerHashAvailable]] to its primary (on the same validator).
  Thus, other primaries will receive the very same worker hashes
   $H_{B_1}$, …, $H_{B_k}$, but indirectly through their workers
   without the need to deal with the actual transaction data.

- Primaries on other validators re-construct the vertex $X$ and commit
   to it by sending a [[HeaderCommitment|signature]] back to the
   creator of the vertex
   (i.e., to the primary that has announced the vertex).
  These primaries also send
   [[TimestampOrderingInformation|transaction ordering information]]
   about transactions referenced in $X$ to all of their validator's
   [[Execution Engines|execution engine's]] [[Shard Engine|shards]].
  The creator then uses these signatures to produce certificates of
   availability $X_A$ and integrity $X_I$ of the vertex.

- The primary $P$ that created the vertex $X$ will collect the vertex
   commitments, fabricate
   [[Availability Certificate|certificates of availability]],
   and broadcast [[AvailabilityCertified|availability certificates]]
   to all primaries when it has received enough signatures
   (namely signatures from a global weak quorum of validators).
  Each of $P$'s vertices after genesis features a certificate of
   availability for $P$'s previous vertex.

- The primary $P$ continues collecting
   [[HeaderCommitment|header commitments]],
   eventually forming learner-specific
   [[IntegrityCertificate|certificates of integrity]],
   which it broadcasts to all relevant primaries.
  The [[IntegrityCertificate|certificate of integrity]] for a specific
   learner proves, according to that learner's Byzantine fault
   tolerance assumptions, that only one such vertex exists for each
   validator at each [[Header Height|vertex height]].
  Thus, the [[Consensus Engine]] requires an
   [[IntegrityCertificate|integrity certificate]] to make vertex $X$
   proposable as an [[Anchor Block|anchor block]].
  As other primaries need to check the validity of anchor block
   proposals, [[IntegrityCertificate|integrity certificates]] are
   broadcast to all validators for the relevant learner(s).
  Proposing and selecting anchor blocks is the principal task of the
   [[Consensus Engine|consensus engine]].
  The [[Execution Engines|execution engine]] eventually executes the
   transaction $T$.

### Consensus

The [[Consensus Engine]] uses Heterogeneous Paxos to establish a
 total order of vertices in the Mempool DAG for each learner.
This in turn implies a total order of transactions.
To this end, Validators on each chain try to achieve consensus on a
 vertex for each height (after genesis).

- When it is a validator's turn to propose a vertex for some height,
   it [[RequestProposal|queries the mempool]] and receives a
   [[PotentialProposal|valid recent vertex]] in response.
  The validator then
  [[HPaxosProposal|proposes this vertex to all the other validators on the chain]].

- Upon receiving a [[HPaxosProposal|proposed vertex]] from another
   validator, the [[Consensus Engine]]
   [[CheckProposal|checks with the mempool]] to see if the proposed
   vertex is known to be valid, and [[PotentialProposal| if it is]],
   then the [[Consensus Engine]]
   [[HPaxosCommitment|responds to all of the other validators]].
  Completing consensus takes at least 2 rounds of
   [[HPaxosCommitment|messages after the proposal]].

- When a validator can prove that a learner has decided on a vertex
   for a height, it broadcasts
   [[HPaxosDecision|the proof of this decision]] to all other
   validators' [[Consensus Engine|consensus engines]], which
   eventually allows consensus to terminate.
  It also sends its own [[Execution Engines|execution engine's]]
   [[Shard Engine|shards]] the [[AnchorChosen|chosen vertex]],
   so they can learn the total order of vertices, and by extension,
   transactions.

### Execution

- When the [[Worker Engine|mempool worker]] sends the
   [[Execution Engines|execution engine]] a
   [[ExecuteTransaction|transaction]] $T$, a new
   [[Executor Engine|Executor]] spins up.
  State within the replicated state machine is divided into Key-Value pairs.
  For each portion of Key space $T$'s label permits it to read or
   write, it [[KVSAcquireLock|acquires a lock]] on the appropriate
   [[Shard Engine|shards]].
  For a transparent asset transfer, the keys read store proofs
   that the sender has the asset (and has not yet transfered it), and
   the keys written store proofs that the sender has transferred
   the asset.
  Note that some keys can be both read and written.

- For each key read, when the relevant [[Shard Engine|Shard]] learns
   the precise data to be read at that time (identifies a unique
   previous transaction and learns the data written by that
   transaction), it [[KVSRead|communicates that data]] to the
   [[Executor Engine|executor]].
  As an optimization, we also allow for _lazy reads_, for which the
   [[Shard Engine|Shard]] won't bother to actually send the
   [[Executor Engine|executor]] the [[KVSRead|data read]] unless, as
   part of running $T$, the [[Executor Engine|executor]]
   [[KVSReadRequest|requests the data]].
  The process by which [[Shard Engine|Shards]] determine when a value
   can be read is complex, and detailed in the
   [[Execution|execution engine page]].

- While running $T$, when the [[Executor Engine|executor]] learns any
   final value to be written to a key, it
   [[KVSWrite|informs the relevant shards]].

- Transaction $T$ can instruct the [[Executor Engine|executor]] to
   perform other side effects
   (such as sending messages to the client), so long as the state
   changes $T$ makes remain deterministic, depending only on $T$ and
   on the values read.

- If $T$ completes without writing values to some of the keys on which
   it has write locks,
       it [[KVSWrite|informs the relevant shards that they should not update those values]].

- When $T$ completes, it
   [[ExecutorFinished|informs the mempool worker]] that this
   transaction is finished.
  This information is later used for garbage collection.

## Certificates and the Mempool DAG

Availability and integrity certificates describe a “global” mempool ᴅᴀɢ consisting of two types of edges:
primary-specific ones and learner-specific ones.
Primary-specific edges correspond to certificates of availability;
they are of out-degree one (except for degree zero for genesis nodes) and
they point to _the_ previous vertex that the primary has produced.
Lerner-specific edges correspond to signatures of signed quorums,
are optional,
and they are forbidden as outgoing edges of genesis vertices;
each signature of a signed quorum of a vertex corresponds to
an outgoing edge that points to the vertex that was signed
and is labeled with the primary that signed the vertex.
The following properties hold:
- all paths to genesis vertices from a given vertex are of the same length and, moreover,
  contain the same number of edges for each learner,
  which means that it makes sense to define for each vertex a unique _height_ relative to each learner
- every pair of outgoing learner-specific edges of the same learner that have the same primary label must
  point to different targets
- the set of primary labels of outgoing edges of every vertex form
  a learner-specific quorum (for the learner-specific vertex height).

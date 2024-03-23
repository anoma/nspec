# Primary

<!--
The primary is responsible for creating vertices from worker hashes
and communicating these to the consensus as anchor block proposals.
The collection of all primary engines jointly create a "global" ᴅᴀɢ of headers,
in which learner-specific ᴅᴀɢs exists as sub-graphs.
-->

## [`NewWorkerHash`](primary/new-worker-hash.md) from [Worker](worker.md)

<!--
- [`HeaderCommitment`](primary/header-commitment.md) → Primary  
  The primary commits to storing the data referenced by its header.
-->

<!--
- [`HeaderAnnoundement`](primary/header-announcement.md) → Primary  
  A new vertex is announced and broadcast to primaries.
-->

- `BlockSurrogate` → Execution  
    
<!--
## [`WorkerHashAvailable`](primary/worker-hash-available.md) from [Worker](worker.md)

- [`HeaderCommitment`](primary/header-commitment.md) → Primary  
  The primary commits to storing the data referenced by a received header.
  
- [`AvailabilityCertified`](primary/availability-certificate.md) → Primary  
  A new availability certificate for a header is broadcast to all primaries.

-->
<!--
## [`HeaderCommitment`](primary/header-commitment.md) from Primary

- [`AvailabilityCertificate`](primary/availability-certificate.md) → Primary  
  A new availability certificate for a header is broadcast to all primaries.

- `IntegrityCertificate` → Primary  
  A new learner-specific integrity certificate for a block header is sent to all primaries of the respective learner.
-->

<!--
- [`PotentialProposal`](../consensus/potential-proposal.md) → [Consensus](../consensus-v1.md)   
  A new learner-specific block is sent to consensus ‼ after a [`RequestProposal`](primary/request-proposal.md) or [`PotentialProposal`](../consensus/potential-proposal.md).
-->

<!--
## `NewBlock` from Primary

- [`NewQuorums`](primary/new-quorums.md) → Primary  
  A new learner-specific signed quorum is sent to all primaries of the respective learner.

- [`HeaderCommitment`](primary/header-commitment.md) → Primary  
  A new header (using the new signed quorum) is announced and broadcast to primaries.

-->

<!--
## [`CheckProposal`](primary/check-proposal.md) from [Consensus](../consensus-v1.md)
- [`PotentialProposal`](../consensus/potential-proposal.md) → [Consensus](../consensus-v1.md)   
  let [Consensus](../consensus-v1.md) know if this is a valid proposal (i.e. it's actually a header in the DAG), or if some conflicting header exists. This may require waiting until some [`HeaderCommitment`](primary/header-commitment.md) arrives. 
-->
<!--
## [`RequestProposal`](primary/request-proposal.md) from [Consensus](../consensus-v1.md)
- [`PotentialProposal`](../consensus/potential-proposal.md) → [Consensus](../consensus-v1.md)   
  Send [Consensus](../consensus-v1.md) a Header suitable to be committed as the next anchor block, if any are available. Otherwise, wait until one is available and then send it.
-->

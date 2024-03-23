#### CheckProposal
- _from_ [Consensus](#Consensus)

##### Purpose
<!-- ANCHOR: purpose -->
Requests that the Mempool check whether this Proposal is valid.
<!-- ANCHOR_END: purpose -->

##### Structure
| Field | Type | Description |
|-------|------|-------------|
| `chain_id` | [`ChainId`](../../types/allofthem-v1.md#chainid) | the chain id |
| `payload`  | [`HeaderFingerprint`](#HeaderFingerprint) | the fingerprint of the block |

##### Effects
- If the check cannot be performed instantly, record the need to answer this request.

##### Triggers

- _to_ [Consensus](#Consensus): [`PotentialProposal`](../../consensus/potential-proposal.md)
  `if` the header is known or a conflicting header is present  
  `then` answer the request accordingly  

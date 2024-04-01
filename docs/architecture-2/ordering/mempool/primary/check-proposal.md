#### CheckProposal
- _from_ [Consensus](#Consensus)

##### Purpose
<!-- --8<-- [start:purpose] -->
Requests that the Mempool check whether this Proposal is valid.
<!-- --8<-- [end:purpose] -->

##### Structure
| Field | Type | Description |
|-------|------|-------------|
| `chain_id` | [`ChainId`](../../types/allofthem.md#chainid) | the chain id |
| `payload`  | [`HeaderFingerprint`](#HeaderFingerprint) | the fingerprint of the block |

##### Effects
- If the check cannot be performed instantly, record the need to answer this request.

##### Triggers

- _to_ [Consensus](#Consensus): [`PotentialProposal`](../../consensus/potential-proposal.md)
  `if` the header is known or a conflicting header is present
  `then` answer the request accordingly

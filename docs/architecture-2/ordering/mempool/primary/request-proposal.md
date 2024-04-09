#### RequestProposal

- _from_ [Consensus](../../consensus-v1.md)

##### Purpose

<!-- --8<-- [start:purpose] -->
Consensus is requesting the next anchor block to propose.
<!-- --8<-- [end:purpose] -->

##### Structure

| Field | Type | Description |
|-------|------|-------------|
| `chain_id` | [[Common types#chainid|`ChainId`]] | the chain in question |

##### Effects

- The newest fresh proposal is sent _or_ the next anchor block will be sent.

##### Triggers

- _to_ [Consensus](../../consensus-v1.md): [`PotentialProposal`](../../consensus/potential-proposal.md)
  `if` a fresh proposal is ready
  `then` send the fresh proposal to consensus

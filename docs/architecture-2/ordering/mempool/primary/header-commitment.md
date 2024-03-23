# HeaderCommitment
- _from_ [[Primary Engine|primary]]

## Purpose
<!-- ANCHOR: blurb -->
Sending a signature to the recipient such that
the latter may fabricate certificates of integrity and/or availability for
a [[Header Vertex|header vertex]] (previously announced by the recipient).
<!-- ANCHOR_END: blurb -->

## Structure
| Field          | Type                 | Description                                               |
|----------------|----------------------|-----------------------------------------------------------|
| `fingerprint`  | [[HdVtxFingerprint]] | the fingerprint of the signed header vertex               |
| `availability` | Boolean              | true if the signature is also w.r.t. availability         |
| `signature`    | bytes                | the signature of the primary, voting for vertex integrity |

The signature is taken over the pair of the fingerprint _and_ the availability flag,
which leads to different signatures different for integrity only and combined commitments.


## Effects
- The primary stores the signature to form a certificate of availability and/or integrity
  unless already sufficiently many signatures were received.
- This might complete the formation of a learner-specific block to be proposed.
- This might complete the validity check of a proposal that was received by consensus.

## Triggers
- to [[Primary Engine|primaries]]: [[AvailabilityCertified]]  
  `if`
  the received signature completes the availability certificate of the header vertex  
  `then`
  the certificate is formed and broadcast to all (relevant) primaries
- to [Primary](../primary.md): [`IntegrityCertificate`](./integrity-certificate.md)  
  `if` the received signature completes some integrity certificate of the header vertex  
  `then` send each of the completed integrity certificates to all relevant validators
- to [Consensus](../../consensus-v1.md): [`PotentialProposal`](../../consensus/potential-proposal.md)  
  `if` there is a pending request for a proposal  
  `then` sent the new block as the best candidate for a proposal.  





#### HeaderAnnouncement

- _from_ [Primary](../primary.md)

##### Purpose

<!-- --8<-- [start:blurb] -->
A primary announces a new header via a fingerprint so that other primaries can respond with signatures over the relevant header.
<!-- --8<-- [end:blurb] -->

##### Structure

| Field | Type | Description |
|-------|------|-------------|
| `fingerprint` | [`HeaderFingerprint`](#HeaderFingerprint) | a "descriptor" of the announced header |

##### Effects

- The receiving Primary deduces the contents of the announced header.

##### Triggers

- to [Primary](../primary.md): [HeaderCommitment](./header-commitment.md)
  `if` all relevant worker hashes are known
  _and_ there is sufficient storage
  `then` re-construct the header, sign the header, and send the signature to the creator of the header

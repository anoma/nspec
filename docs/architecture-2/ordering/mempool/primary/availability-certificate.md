#### AvailabilityCertified

- _from_ [Primary](../primary.md)

##### Purpose

<!-- --8<-- [start:blurb] -->
The certificate informs the validator about availability of a header
and who has taken on the responsibility of availability.
<!-- --8<-- [end:blurb] -->

##### Structure

| Field         | Type                                                  | Description                            |
|---------------|-------------------------------------------------------|----------------------------------------|
| `fingerprint` | [`HeaderFingerprint`](#HeaderFingerprint)             | the header that is certified           |
| `certificate` | [`AvailabilityCertificate`](#AvailabilityCertificate) | the broadcast availability certificate |

##### Effects

- Receiving the availability certificate means that all further signatures only concern integrity.

##### Triggers

(none)

<!--  why do we broadcast this one? https://github.com/anoma/specs/issues/178 -->

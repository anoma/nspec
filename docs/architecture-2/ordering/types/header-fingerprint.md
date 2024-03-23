# `HeaderFingerprint`

The header fingerprint describes an actual header succinctly,
using easily available information.

| Field       | Type                   | Description                                                                             |
|-------------|------------------------|-----------------------------------------------------------------------------------------|
| `id`        | [[Id]]                 | the ɪᴅ of the primary engine that created the header                                    |
| `height`    | natural number         | the height in the header chain of the same primary                                      |
| `batches`   | [[WHFingerprint]] list | a list of worker hash fingerprints, referencing a list of batches                       |
| `cert_hash` | [[Hash]]               | the hash of the availability certificate of the previous header (unless at height zero) |


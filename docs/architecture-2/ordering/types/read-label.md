# ReadLabel

## Purpose

The ReadLabel specifies which keys a transaction may and will read from.
The rationale behind this information is that
if a transaction definitely reads from a set of keys,
the corresponding [[KVSReadRequest]]s can be issued even
before spawning an executor.

## Structure

| Field       | Type           | Description                                            |
|-------------|----------------|--------------------------------------------------------|
| `will_read` | [[KVSKey]] set | in V1, this is a generic set of keys that will be read |
| `may_read`  | [[KVSKey]] set | in V1, this is a generic set of keys that may be read  |

From V2 onward,
after imposing a tree-structure on keys (or something similar),
we can represent potentially infinite sets of keys.

## Notes

Occasionally,
we refer to "may read"-keys also as lazy reads
as they potentially only issued on demand.

<!--
This is *not* a message in its own right, but this type is used in the fields of other messages.
-->

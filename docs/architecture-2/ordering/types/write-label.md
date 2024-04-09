# WriteLabel


## Purpose

The WriteLabel specifies which keys a transaction may and will write to.
The rationale behind this information is that
if a transaction definitely write to a set of keys,
there is no need to wait for previous read or writes to this key.
<!--
handling "may write"s in the most efficient manner is actually
quite the challenge!
-->

## Structure


| Field       | Type           | Description                                            |
|-------------|----------------|--------------------------------------------------------|
| `will_write` | [[KVSKey]] set | in V1, this is a generic set of keys that will be written |
| `may_write`  | [[KVSKey]] set | in V1, this is a generic set of keys that may be written  |

From V2 onward,
after imposing a tree-structure on keys (or something similar),
we can represent potentially infinite sets of keys.


<!--
This is *not* a message in its own right, but this type is used in the fields of other messages.
-->

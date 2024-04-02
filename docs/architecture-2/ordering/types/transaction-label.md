# TransactionLabel

## Purpose

Specifies which keys a transaction execution may/will read/write.

## Structure

| Field   | Type           | Description                                  |
|---------|----------------|----------------------------------------------|
| `read`  | [[ReadLabel]]  | the keys a transaction may or must read from |
| `write` | [[WriteLabel]] | the keys a transaction may or must write to  |

<!--
This is *not* a message in its own right, but this type is used in the fields of other messages.
-->

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TransactionCandidate

The basic unit of data that users send to
the [[Mempool Engines|mempool]] for the purpose of ordering and execution
(aka [processing](https://en.wikipedia.org/wiki/Transaction_processing))
as part of a [[TransactionRequest|transaction request]] is called a _transaction candidate_.

| Field        | Type                      | Description                             |
|--------------|---------------------------|-----------------------------------------|
| `label`      | [[TransactionLabel]]      | keys that may/will be read/written      |
| `executable` | [[TransactionExecutable]] | the payload for post-ordering execution |

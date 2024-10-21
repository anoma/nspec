---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TransactionExecutable

All information about what to do after a transaction is ordered, e.g., calculations, or proof checks,
is given by a string of bytes that we call _transaction executable_.

The transaction executable must be able to be run on a known virtual machine. Execution will be gas-metered,
and execution which exceeds the gas limit specified in the [[TransactionCandidate]] will fail. Execution
must return a [[Transaction]] object.
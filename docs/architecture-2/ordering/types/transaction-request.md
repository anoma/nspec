---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TransactionRequest

## Description

Transaction requests are the wrapper for
[[TransactionCandidate|transaction candidates]]
and provide additional information about 
the submitted transaction candidate or its context.
See [[TransactionCandidate|transaction candidate]] for more information.

## Datatype

| Field          | Type                     | Description                          |
|----------------|--------------------------|--------------------------------------|
| `tx`           | [[TransactionCandidate]] | the actual transaction candidate to be ordered |
| `reply_to` | [[ExternalIdentity]] option | optional indication for who would receive information about the status of the request besides the information given in the transaction candidate itself |
| `resubmission` | [[TxFingerprint]] option | optional reference to a previous occurrence of the same transaction candidate (if existing and/or relevant)|

The resubmission indicates if there was a previous occurrence of
the very same transaction candidate which either has failed or
a needs to be executed again, e.g., because it is a recurring payment.


!!! todo

  lists of receivers/senders are static
  and thus could be listed here as well

## List of receivers

- [[Worker Engine|Worker]]

## List of senders

- [[User]]
- [[Solver]]


!!! todo

	make guidelines for when to include "addressing" information
	in "semantic" data type/structure; here, for TransactionRequest
	we have it, 
	but maybe the requetor_id is better captured by
	generic information flow control?

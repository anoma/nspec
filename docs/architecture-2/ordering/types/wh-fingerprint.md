# `WHFingerprint`


The fingerprint of a worker hash.

| Field       | Type           | Description                                                   |
|-------------|----------------|---------------------------------------------------------------|
| `id`        | [[Id]]         | the ɪᴅ of the worker engine that created the worker hash      |
| `batch_no`  | natural number | the number of the batch into which the transaction was packed |
| `length`    | natural number | the number of transactions in the batch                       |
| `signature` | bytes          | the signature over the hash of the actual transaction list    |

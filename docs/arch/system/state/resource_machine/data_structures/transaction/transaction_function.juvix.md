---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.transaction.transaction_function;
```

# Transaction Function

A transaction function `TransactionFunction` is a function that outputs a transaction: `transactionFunction() -> Transaction`.

Transaction functions take no input but can perform I/O operations to read information about global state either by reading data at the specified global storage address or by fetching data by index. The requirements for transaction functions are further described in [[Transaction function format]].
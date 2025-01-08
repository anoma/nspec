---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - resource-machine
  - protocol
  - commitment
  - nullifier
  - accumulator
  - resource logic
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.resource_machine;
    import prelude open;
    import arch.system.types.transaction open;
    ```

# Resource Machines

A **resource machine** is a term of type `ResourceMachine`.

## `ResourceMachine`

```juvix
trait
type ResourceMachine := mkResourceMachine {
  createTransaction :
    -- CMTreeRoots : Set CMtree.Value;
    -- actions : Set Action;
    -- deltaProof : DeltaProvingSystem.Proof;
    Unit -> Transaction; -- which is the mkTransaction function
  composeTransactions : Transaction -> Transaction -> Transaction;
  verifyTransaction : Transaction -> Bool;
  -- read nullifier set?
  -- append to nullifier set?
  -- read commitment tree?
  -- add data to commitment tree?
};
```

## Purpose

The purpose of the `ResourceMachine` is to allow us to:

- create a transaction,
- compose transactions, and
- verify transactions according to the rules of the protocol.

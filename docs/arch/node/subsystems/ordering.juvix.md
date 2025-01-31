---
icon: material/order-alphabetical-ascending
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - ordering-subsystem
  - index
---

???+ code "Juvix imports"

  ```juvix
  module arch.node.subsystems.ordering;
  import arch.node.engines.executor open;
  import arch.node.engines.mempool_worker open;
  ```

# Ordering Subsystem

---

## Purpose

The *Ordering Subsystem* is responsible for ordering transactions in the node.

---

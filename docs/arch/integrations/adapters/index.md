---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - index
  - resource-machine
  - protocol-adapter
---

# Protocol Adapters

A protocol adapter provides [[Executor Engine|executor engine]] and [[Shard Engine|shard engine]] functionality on a foreign blockchain protocol (adaptee) being independent of the Anoma protocol (target). In other words, it processes [[Resource Machine]] transactions and updates the RM state.

In order to support a protocol adapter, the adaptee protocol has to be programmable (i.e., support smart contracts).

## Instances

- [[Ethereum Virtual Machine]] protocol adapter prototype (settlement-only)

---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - index
  - work-in-progress
  - resource-machine
  - protocol-adapter
---

# Protocol Adapters

Protocol adapters are programs settling resource machine transactions on foreign blockchain protocols (adaptees) that are independent of the Anoma protocol (target).

This requires the adaptee protocol to be programmable (i.e., support smart contracts).

## Transaction Function Evaluation

Protocol adapters can be distinguished by their ability to partially evaluate transaction functions.

The current protocol adapter is **settlment-only**. It can only fully-evaluated transaction functions resulting in a static and fully determined transaction candidate.

<!-- TODO Improve explanation -->

**Full** protocol adapters implement the full executor behavior and can allow adding timestamps or other data post-ordering.

<!-- TODO Add link to executor specs -->

---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - index
---

# Node Architecture
​
The operational architecture specification concerns the state evolution of Anoma instances, broken into smaller steps: which messages are exchanged, how computation is performed on the level of function calls, and which intermediate states are reachable.
The specification is organized into the following sections:

- [[Hardware Subsystem]]

- [[Identity Subsystem]]

- [[Ordering Subsystem]]

- [[Network Subsystem]]

## Message Flow

<figure markdown>

![Message Diagram](transaction_flow.svg)


<figcaption markdow

Intent/transaction candidate flowchart.

</figcaption>
</figure>

---
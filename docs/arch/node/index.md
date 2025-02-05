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
The node architecture specification concerns the state evolution of Anoma instances,
broken into smaller steps[^1] on the level of [[Engine|engines]] in nodes:
- which messages are sent and received,
- which computation is performed as reaction to message receptions, and
- which local state changes ensue as a result.

How message passing works is introduced in the [[Anomian]],
based on illustrative examples.
On a higher level,
we have a static pattern that connects two engine types with a message type
if messages of this type can be sent between engine instances of the two types.
An illustration of the pattern of communication between participants<!--
-->—how they may send messages to each other—<!--
-->is given in the following figure.

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

[^1]: The technical term is the _isolated turn principle_ [@taxonomy-of-actor-models-2016].

---
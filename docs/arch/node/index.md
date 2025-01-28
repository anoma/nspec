---
icon: material/graph
search:
  exclude: false
  boost: 2
---

# Introduction
​
The node architecture specification concerns the state evolution of Anoma instances,
broken into smaller steps[^1] on the level of [[Engine|engines]] in nodes:
which messages are sent and received,
which computation is performed as reaction to message receptions, and
which local state changes ensue as a result.

How message passing works is introduced in the [[Anomian]],
based on illustrative examples.
On a higher level,
we have a static pattern that connects to engine types with a message
if messages of the respective can be sent between them.
An illustration of the pattern of communication between participants<!--
-->—how they may send messages to each other—<!--
-->is given in the following figure.


<!--TODO: Can we make this diagram in korki so we can edit it easily? -->
<figure markdown>

![Message Diagram](transaction_flow.svg)

<figcaption markdow

Intent/ transaction candidate flowchart.

</figcaption>
</figure>

The specification is organized into the following sections:

- [[Hardware Component]]

- [[Identity Component]]

- [[Ordering Component]]

- [[Networking Component]] (coming soon)

[^1]: The technical term is _isolated turn principle_ [@taxonomy-of-actor-models-2016].

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Basic Concepts

## Node

A node is run within and by an agent. Specifically, we can say that the agent dedicates a certain amount of storage, compute, and bandwidth resources to the node (these can change over time), configures it with their preferences, and the node runs autonomously using those resources, periodically soliciting or responding to inputs from the agent.

In general, we assume that the node runs the protocol as defined in these specification documents. Other nodes running other protocols (including nodes on agents who have modified their implementation of the protocol) are out-of-scope, except insofar as we care about modeling arbitrary software run by potentially Byzantine parties.

## Observation

Observations are made by agents. One kind of observations (name: TBD?) are made through the node, i.e. observations of state, and we want to reason about this kind for e.g. safety properties. The other kind are arbitrary observations by agents, and we want to reason about this kind for e.g. bounded disclosure properties (since malicious agents might not follow the protocol).=
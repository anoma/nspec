---
icon: simple/awsorganizations
search:
  exclude: false
  boost: 2
tags:
  - index
---

# Anoma architecture

The Anoma architecture is the blueprint that defines the structure and behaviour
of the components that make up the Anoma protocol. There are two high-level
components: the Node architecture and the System architecture.

## Node architecture

Details the internal composition of individual nodes:

- [[Engine|Engine-based modular architecture]]
- [[Anoma Message|Inter-engine communication protocols]]
- [[Engine Behaviour|Engine-specific behaviours and responsibilities]]


## System architecture

Defines the high-level structure and behaviour of the distributed network,
including:

- Distributed state management <!-- and consensus -->
- Core data types and data flow for Network operations
- System-wide properties and guarantees

---
icon: simple/awsorganizations
search:
  exclude: false
  boost: 2
tags:
- protocol-architecture
---

# Protocol Architecture

The Anoma architecture is the blueprint that defines the structure and behaviour of
the Anoma system. It consists of two main components that work together to
create a robust distributed system, the [[System Architecture|system architecture]]
and the [[Node Architecture|node architecture]].

## [[System Architecture]]
   
Defines the high-level structure and behaviour of the distributed network,
including:

- Network topology and communication patterns
- Distributed state management <!-- and consensus -->
- Core data types and data flow
- System-wide properties and guarantees

## [[Node Architecture]]
   
Details the internal composition of individual nodes:

- [[Engine|Engine-based modular architecture]]
- [[Anoma Message|Inter-engine communication protocols]]
- [[Engine Behaviour|Engine-specific behaviours and responsibilities]]
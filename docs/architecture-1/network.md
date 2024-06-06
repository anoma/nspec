---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Network Architecture

# Introduction

## Design overview

The network and software architecture described in the following
is based on the actor model,
compositional cryptographic identities,
a modular transport & routing system
and a sovereign domain system.

Actors communicate via asynchronous message passing,
and are addressed using their cryptographic identities.

An *engine* is a software module that implements the behavior of an actor.

An *engine instance* is a running instance of an engine with an associated cryptographic identity.

A *node* is a set of engine instances
that consists of a *transport* and a *router* engine instance as the minimum,
and any additional engine instances according to the local configuration.
The *node identity* is defined as the identity of its *router engine instance*.

Cryptographical identities are compositional,
and refer to either individual actors or a group of actors.

The system supports unicast, multicast (pub/sub), and anycast communication patterns,
which is chosen according to the type of the destination identity.

Each message is authenticated by its sender using a cryptographic signature,
addressed to a cryptographic identity,
and contains a payload with an associated versioned protocol identifier.
A message to a compositional identity may induce either unicast, multicast, or anycast communication,
depending on the number of identities it is composed of.

The basic communication primitive is unreliable, unordered delivery of unicast messages between engines,
via a modular transport system that supports various transport protocols.
Based on this underlying primitive,
reliable unicast and reliable multicast protocols offer reliable causal delivery semantics.

Messages are routed based on their destination identity using a modular routing system,
where a routing protocol is chosen according to the type of the destination.
Destination identities are associated with node identities and transport addresses
using self-signed advertisements that are disseminated over the network
via peer-to-peer protocols and out-of-band means.

During message sending, the routing and transport system
takes into account information flow preferences and constraints,
including node trust, reputation, and measurements.

The network architecture consists of heterogenous, sovereign domains,
each of which induce its own peer-to-peer overlay.
Each domain has an owner with an associated compositional identity,
which has the authority to define the domain configuration,
that includes the protocols used together with their configuration parameters,
the list of externally advertised nodes that accept join and other requests,
authentication mechanism to join the domain.

The network architecture supports grassroots domains,
which may be instantiated in multiple disjoint locations
and thus do not rely on global resources that must be always available.

Each domain has a choice over the protocols it runs,
which typically includes a membership and overlay maintenance protocol,
a multicast message dissemination protocol with publish-subscribe semantics,
and a content-addressed block storage protocol.

## Overview

The network architecture follows from the system model we laid out in the previous sections.

The basic communication primitive is unicast communication between engines,
where each engine is addressed by its cryptographic identity.
A node consists of multiple engines, and has one or more transport addresses.

## Addressing

Nodes, engines, and domains are addressed by their cryptographic identities.
The node address is defined as the identity of the *Router Engine* of the node.

In order to send a message to an engine,
two pieces of information are necessary:
the identity of the node that hosts the engine,
and the transport addresses of the node.

Signed advertisement messages are used to bind addresses together from different layers:
- *NodeAdvert*: binds a node address to transport addresses
- *EngineAdvert*: binds an engine address to a node address
- *DomainAdvert*: binds a domain address with node addresses

These are transmitted either as part of network protocols between nodes or out of band,
and are stored locally by each node.

## Transport

Nodes establish and maintain network connections
among each other using a modular transport system
that provides encrypted transport channels between nodes.

Each node maintains a pool of open connections to other nodes,
and reuses them whenever a message needs to be sent to one of the connected nodes.

The modular transport architecture allows a node to support various transport protocols,
such as protocols over IP, public-key addressed overlay networks,
mesh networks, and delay-tolerant networks.

Transport protocols provide authenticated and encrypted connections with forward secrecy.
Message ordering and reliability guarantees may vary per message,
an appropriate transport protocol is selected
according to transport constraints and requirements of outgoing messages.

## Routing

Each node has a message router
that is responsible for forwarding both intra-node and inter-node messages between engine instances.
It forwards intra-node messages directly between local engines,
and sends and receives inter-node messages via the transport system.

Inter-node messages are authenticated by signatures,
the router is responsible for signing outgoing and verifying incoming messages.

Both the source and destination address of a message is an *external identity*.
The router makes routing decisions based on this.

The source address always belongs to the identity of the engine instance that sent it,
while the destination address can belong to either an engine instance, a domain, or a pub/sub topic,
which corresponds to unicast, anycast, and multicast communication patterns, respectively.

A unicast message is sent between two (local or remote) engine instances,
an anycast message is sent from an engine instance to any member of a domain,
while a pub/sub message is sent from an engine instance to all subscribers of a topic.

## Domains

The network consists of heterogenous, sovereign domains.
A domain is identified by a compositional identity.
This identity is the authority
that defines the protocols used in the domain and their configuration,
the authentication mechanism used to join the domain,
permissions for its members,
and the list of publicly advertised nodes
for non-members to send join and other requests to the domain.

The minimum set of protocols supported by a domain are:
a membership protocol, dissemination protocol, and block storage protocol.

A domain may have multiple disjoint instances in different locations.
Each domain instance induces its own peer-to-peer overlay network,
and may run a different set of protocols,
as appropriate to the underlying physical network.

Typically, a domain consists of a core network of always-on servers with low to moderate churn,
and multiple edge networks in different locations of end-user devices with high-churn.
In the core network the dissemination protocols are
either a full mesh in the simplest case for a small number of peers,
or a multi-hop peer-to-peer dissemination protocol that scales to a larger number of nodes.
On edge networks, dissemination protocols may use
IP multicast, wireless mesh network, and delay-tolerant network protocols.

In the following, we solely focus on core network protocols,
(edge network protocols remain future work),
and define a set of membership, dissemination and block storage protocols.

### Joining a domain

In order to join a domain, a node needs to have a *DomainAdvert* available locally,
which may be obtained either out-of-band and added to the node configuration,
or via *inter-domain protocols*
that enable anycast routing of messages based on the domain identity to domain members,
who can return the latest version of *DomainAdvert* upon request,
as well as accept join requests.

The *DomainAdvert* specifies one or more introducer nodes to send the *JoinRequest* to,
as well as the authentication mechanism used,
and is signed by the domain's cryptographic identity.

Authentication mechanisms initially supported are:
- No authentication
- Pre-Shared Key (PSK)

When the join request is approved, the responder adds the new member to the set of domain members.

Once joined, a new member may connect to other domain members,
and send messages according to the protocols defined in the domain configuration.

### Membership

The domain membership protocol maintains a full view of members.
This is achieved using a Blocklace [@blocklace] data structure,
which contains a DAG of operations on a CRDT,
and is synchronized among all members.

The CRDT used is a permissioned Map with Last-Write Win (LWW) update semantics,
where the set of keys are maintained as an Observed-Remove Set (OR-Set),
and the value associated with a key is a LWW register.

---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Networking Machine

## Purpose

The Networking Machine is responsible for message passing between engine instances,
both locally (intra-node), and over the network (inter-node).
The core functionality includes message routing and transport,
upon which more complex peer-to-peer (P2P) protocols are built.

## Scope

Initially, the Anoma network is limited to the following.

- The network consists of multiple nodes that can establish direct connections with each other over QUIC/TLS transport protocols.

- Nodes know about each other's addresses by explicitly adding [[NodeAdvert]]s to their configuration.

- Engine instances can send and receive unicast and multicast (pub/sub) messages, both locally and over the network.

- Pub/sub is limited to a single publisher with directly connected local and remote subscribers (no multi-hop routing yet).

Later, the Anoma network is going to support domains, dynamic P2P overlays, and P2P routing protocols.

Domains are described in *[P2P Overlay Domains with Sovereignty](https://arxiv.org/abs/2306.16153) (PODS)*.
In PODS, the network architecture consists of a collection of *nodes* that are part of one or multiple heterogeneous *domains*.
Each domain has its own overlay topology, and a distinct set of P2P *intra-domain protocols*, tailored to the characteristics and needs of the nodes in that domain.

## Overview

### Terminology

<!-- --8<-- [start:node] -->
A *node* is the set of running *engine instances* that collectively participate in the network under a single *node identity*.
A *peer* is a connected neighbour of a *node* in the network.
<!-- --8<-- [end:node] -->
<!-- --8<-- [start:node-id] -->
The *[[NodeIdentity|node identity]]* is the cryptographic identifier of the node, and is used for addressing messages and signing *[[NodeAdvert|node advertisements]]*.
<!-- --8<-- [end:node-id] -->

### Message passing

Communication between [[Engine Families|engine instances]]
is inspired by the actor model
via asynchronous message passing among them.

Communicating engine instances can reside either on the same node
or on different nodes connected over the network.

A message received by an engine instance may trigger reactions
in the form of one or more messages sent by the receiver.
Typical reactions to a message include
a response to a request in the often used request-response pattern,
or a forwarding decision in a network protocol.

### Message transmission, addressing, routing

Message transmission in the network is either
one-to-one (unicast), few-to-many (multicast), or one-to-any (anycast).

A unicast message is sent between two engines by a single sender to a single recipient.
It is sent over the network either directly to the destination or over multiple hops,
depending on the transport protocol used.

Multicast messaging is underlying the topic-based publish-subscribe (pub/sub) pattern,
where a message (a.k.a. event) is sent by an authorized publisher to all subscribers of the topic,
and sent over the network from one of the publishers towards all subscribers,
either via direct connections in a hub-and-spoke topology,
or along multi-hop paths, often in a tree topology.

Anycast messages are used when sending a request to any known member of a domain.

An [[EngineMessage]] is addressed from a *source* [[EngineIdentity|engine identity]] to a *destination* [[ExternalIdentity|external identity]],
and the content of the message is authenticated by a signature of the source engine.
The destination identity is either
a [[NodeIdentity]] or [[EngineIdentity]] (for unicast messages),
a pub/sub [[TopicIdentity]] (for multicast messages),
or a [[DomainIdentity]] (for anycast messages).

The [[Router]] engine of each node is responsible for message routing
between local engines, local and remote engines,
and in some cases relaying between two remote engines.
It makes routing decisions based on the destination identity in the message.

### Message flow

#### Intra-node unicast & multicast messages

<figure markdown="span">

![Inter-node messages](node.dot.svg){ width="450" }
--8<-- "networking/node/index.md:fig-node-caption"
</figure>

#### Inter-node unicast messages

<figure class="invertable wide" markdown="span">

![Unicast message](unicast.dot.svg){ width="450" }
--8<-- "networking/node/index.md:fig-unicast-caption"
</figure>

#### Inter-node multicast messages

<figure class="invertable wide img-max" markdown="span">

![Multicast message](multicast.dot.svg){ width="450" }
--8<-- "networking/intra_domain/index.md:fig-multicast-caption"
</figure>

## Network architecture

The network consists of several sovereign domains with heterogenous protocols,
where each domain maintains its own peer-to-peer overlay topology,
manages its own membership,
and determines the set of protocols that run inside the domain.
A set of inter_domain protocols are responsible for
clustering nodes based on domain membership
and routing anycast messages to domains.

### Intra-domain protocols

<div class="v2" markdown>

Inside each domain, a [[Domain]] membership and an overlay [[Topology]] maintenance protocol
are responsible for responding to membership decisions,
as well as keeping the overlay connected and keeping track of a partial view of online members.

</div>

The P2P [[PubSub]] (publish-subscribe) protocol is responsible for event dissemination
from authorized publishers to subscribers,
while the P2P [[Storage]] protocol offers block storage and retrieval.

<div class="v2" markdown>

### Inter-domain protocols

Two inter_domain gossip protocol run in parallel: a Trust-Aware [[Peer Sampling]] (TAPS) and a Trust-Aware [[Clustering]] (TAC) protocol.
The two protocols together construct a small world network, where TAPS provides continuously changing long-range routing links,
while TAC discovers nodes with similar domain membership.
Using trust information in these protocols aids in making these protocols more resilient against eclipse and hub attacks.
TAPS is further enhanced by Uniform Peer Sampling (URPS) that uses statistical analysis to filter out peers over-represented in the peer sampling stream.
Domain membership privacy in TAC is achieved by using the Bloom-and-Flip (BLIP) algorithm that calculates similarity between randomized Bloom filters (see BLIP),
and then calculating the exact overlap using a Private Set Intersection (PSI) protocol.
Participation in the inter_domain protocols is optional: nodes that do not wish to be discovered outside of their domains and have fixed domain membership
may opt out of participating in inter_domain protocols, in order to decrease load, increase security, and thwart potential attacks coming from outsiders (e.g. DDoS).
This allows domains to have internal-only and external-facing members.

There are two ways to interact with a [[Domain]]:
either by sending external requests to any available domain member that may return a reply,
or by joining the domain and participating in the intra-domain protocols.
For both type of requests, a node needs to know about one or more domain members to send the request to,
which can be discovered either via the [[Clustering]] protocol,
or via a lookup request that is routed in the inter_domain overlay using a greedy routing algorithm by the [[Domain Routing]] protocol.
Both methods use domain membership similarity as a distance metric.

</div>

## Software architecture

<figure class="invertable wide" markdown="span">

![Engines of the Networking Machine](engines.dot.svg){ width="450" }

<figcaption markdown="span">

**Engines of the Networking Machine.**
Octagons are engines with a single instance per node.
Double octagons are engines with multiple instances.
Solid arrows mark unicast message flow directions.
Dashed arrows mark multicast notifications.
Dotted arrows mark messages sent via the Router.

</figcaption>
</figure>

### Engines

Engines are grouped based on their scope in the network architecture.

#### Intra-node and inter-node protocols

--8<-- "networking/node/index.md:purpose"

##### Router

The [[Router]] engine is responsible for [[EngineMessage|message]] routing
and handles both inter-node and intra-node messages.
It authenticates received messages by verifying the signature of the *source* identity,
and makes routing decisions based on the *destination* identity.

It also provides topic-based pub/sub functionality for local engines and performs local multicast message routing.

It can also relay messages between two remote nodes,
in which case the [[EngineMessage]] is encrypted and wrapped in a [[RelayMessage]].

The message routing algorithm is described in the [[EngineMessage]] section.

##### Transport

The [[Transport]] engine is responsible for establishing and maintaining encrypted transport connections between peers.
It supports various network transport protocols that are chosen according to transport preferences
set by locally on a per-message or per-node basis, and defaults to the remote node's preferences specified in a [[NodeAdvert]] message.

##### Network Identity Store

The [[Network Identity Store]] engine maintains a [[IdentityStore|data store]] with [[IdentityRecord|records]]
that contain information associated with identities of engines, nodes, pub/sub topics, and domains.

The source of this information can be either local configuration
or advertisements received from other nodes via P2P protocols.

For each [[EngineIdentity]] it stores its local engine address, if applicable to the implementation.

For each [[NodeIdentity]], it stores transport addresses in order of preference, measurements, trust value, and reputation value.

For each [[TopicIdentity]], it stores the [[PubSub]] [[TopicAdvert]].

<div class="v2" markdown>

For each [[DomainIdentity]], it stores the [[DomainAdvert]].

</div>

##### Implementation

!!! note

    Different implementations may organize the Router and Transport components in different ways
    that fit their particular programming model and software architecture.
    Thus engines may communicate via either a single Router as described above,
    or multiple Router instances, one per destination node.

    Furthermore, the Network Identity Store may respond to lookup requests for engine names
    with the local address of the engine instance that can be used to send messages to a local engine directly.
    In case of remote engines when multiple Router engine instances are used,
    it may provide the local address of the Router engine instance that corresponds to the remote node.

#### Intra-domain protocols

--8<-- "networking/intra_domain/index.md:purpose"

#### PubSub

The [[PubSub]] engine implements a P2P topic-based pub/sub protocol and performs inter-node multicast message routing within a domain.

#### Storage

The [[Storage]] engine implements a P2P block storage protocol.


# Networking Machine


## Purpose


The Networking Machine is responsible for message passing between engine instances,
both locally (intra-node), and over the network (inter-node).
The core functionality includes message routing and transport,
upon which more complex peer-to-peer (P2P) protocols are built.

<div class="v1" markdown>


## Scope


The Anoma v1 network is limited to the following.
- The network consists of multiple nodes that can establish direct connections with each other over QUIC/TLS transport protocols.
- Nodes know about each other's addresses by explicitly adding [[NodeAdvert#nodeadvert]]s to their configuration.
- Engines can send unicast and multicast (pub/sub) messages to both local and remote engines.
- Pub/sub is limited to a single publisher with directly connected subscribers.

The Anoma v2 network is going to support domains, dynamic P2P overlays, and P2P routing protocols.
This is described in more detail in *[P2P Overlay Domains with Sovereignty](https://arxiv.org/abs/2306.16153) (PODS)*.
In PODS, the network architecture consists of a collection of *nodes* that are part of one or multiple heterogeneous *domains*.
Each domain has its own overlay topology, and a distinct set of P2P *intra-domain protocols*, tailored to the characteristics and needs of the nodes in that domain.

</div>

## Overview


### Terminology


<!-- --8<-- [start:node] -->
A *node* is the set of running *engine instances* that collectively participate in the network as a single entity.
Each node has a [[Router#router]] engine instance responsible for intra- and inter-node message routing,
and a [[Transport#transport]] engine instance responsible for inter-node connectivity.

A *peer* is a connected neighbor of a *node* in the network.
<!-- --8<-- [end:node] -->
<!-- --8<-- [start:node-id] -->
The *[[NodeIdentity#nodeidentity|node identity]]* in the networking context is the [[EngineIdentity#engineidentity|engine identity]] of the [[Router#router]] engine instance.
<!-- --8<-- [end:node-id] -->

### Message passing


Communication between [[Architecture 2#engine-models|engines]] follows the actor model
with asynchronous message passing between engines.

Communicating engines can reside either on the same node
or on different nodes connected over the network.

A message received by an engine may trigger reactions
in the form of one or more messages sent by the receiver.
A typical reaction is a response to a request
in the often used request-response pattern,
or a forwarding decision in a network protocol.

### Message transmission, addressing, routing


Message transmission in the network is either
one-to-one (unicast), few-to-many (multicast), or one-to-any (anycast).

A unicast message is sent between two engines by a single sender to a single recipient,
and routed over the network either directly to the destination or over multiple hops,
depending on the transport protocol used.

Multicast messaging follows the topic-based publish-subscribe (pub/sub) pattern,
where a message (a.k.a. event) is sent by an authorized publisher to all subscribers of the topic,
and routed over the network along multi-hop paths from a publisher towards subscribers.

Anycast messages are used when sending a request to any known member of a domain.

An [[EngineMessage#enginemessage]] is addressed from a *source* [[EngineIdentity#engineidentity|engine identity]] to a *destination* [[ExternalIdentity#externalidentity|external identity]],
and the content of the message is authenticated by a signature of the source engine.
The destination identity is either
a [[NodeIdentity#nodeidentity]] or [[EngineIdentity#engineidentity]] (for unicast messages),
a pub/sub [[TopicIdentity#topicidentity]] (for multicast messages),
or a [[DomainIdentity#domainidentity]] (for anycast messages).

The [[Router#router]] engine of each node is responsible for message routing
between local engines, local and remote engines,
and in some cases relaying between two remote engines.
It makes routing decisions based on the destination identity in the message.

### Message flow


#### Intra-node unicast & multicast messages



<figure markdown="span">

![Inter-node messages](node.dot.svg){ width="450" }
--8<-- "networking/node.md:fig-node-caption"
</figure>


#### Inter-node unicast messages


<figure class="invertable wide" markdown="span">

![Unicast message](unicast.dot.svg){ width="450" }
--8<-- "networking/node.md:fig-unicast-caption"
</figure>

#### Inter-node multicast messages


<figure class="invertable wide img-max" markdown="span">

![Multicast message](multicast.dot.svg){ width="450" }
--8<-- "networking/intra-domain.md:fig-multicast-caption"
</figure>


## Network architecture


The network consists of several sovereign domains with heterogenous protocols,
where each domain maintains its own peer-to-peer overlay topology,
manages its own membership,
and determines the set of protocols that run inside the domain.
A set of inter-domain protocols are responsible for
clustering nodes based on domain membership
and routing anycast messages to domains.

### Intra-domain protocols


<div class="v2" markdown>

Inside each domain, a [[Domain#domain]] membership and an overlay [[Topology#topology]] maintenance protocol
are responsible for responding to membership decisions,
as well as keeping the overlay connected and keeping track of a partial view of online members.

</div>

The P2P [[PubSub#pubsub]] (publish-subscribe) protocol is responsible for event dissemination
from authorized publishers to subscribers,
while the P2P [[Storage#storage]] protocol offers block storage and retrieval.

<div class="v2" markdown>


### Inter-domain protocols


Two inter-domain gossip protocol run in parallel: a Trust-Aware [[Peer Sampling#peer-sampling]] (TAPS) and a Trust-Aware [[Clustering#clustering]] (TAC) protocol.
The two protocols together construct a small world network, where TAPS provides continuously changing long-range routing links,
while TAC discovers nodes with similar domain membership.
Using trust information in these protocols aids in making these protocols more resilient against eclipse and hub attacks.
TAPS is further enhanced by Uniform Peer Sampling (URPS) that uses statistical analysis to filter out peers over-represented in the peer sampling stream.
Domain membership privacy in TAC is achieved by using the Bloom-and-Flip (BLIP) algorithm that calculates similarity between randomized Bloom filters (see BLIP),
and then calculating the exact overlap using a Private Set Intersection (PSI) protocol.
Participation in the inter-domain protocols is optional: nodes that do not wish to be discovered outside of their domains and have fixed domain membership
may opt out of participating in inter-domain protocols, in order to decrease load, increase security, and thwart potential attacks coming from outsiders (e.g. DDoS).
This allows domains to have internal-only and external-facing members.

There are two ways to interact with a [[Domain#domain]]:
either by sending external requests to any available domain member that may return a reply,
or by joining the domain and participating in the intra-domain protocols.
For both type of requests, a node needs to know about one or more domain members to send the request to,
which can be discovered either via the [[Clustering#clustering]] protocol,
or via a lookup request that is routed in the inter-domain overlay using a greedy routing algorithm by the [[Domain Routing#domain-routing]] protocol.
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


--8<-- "networking/node.md:purpose"

##### Router


The [[Router#router]] engine is responsible for [[EngineMessage#enginemessage|message]] routing
and handles both inter-node and intra-node messages.
It authenticates received messages by verifying the signature of the *source* identity,
and makes routing decisions based on the *destination* identity.

It also provides topic-based pub/sub functionality for local engines and performs local multicast message routing.

It can also relay messages between two remote nodes,
in which case the [[EngineMessage#enginemessage]] is encrypted and wrapped in a [[RelayMessage#relaymessage]].

The message routing algorithm is described in the [[EngineMessage#enginemessage]] section.


!!! note

    An implementation may optimize intra-node messaging between local engine instances, such that they communicate directly instead of via the router.

##### Transport


The [[Transport#transport]] engine is responsible for establishing and maintaining encrypted transport connections between peers.
It supports various network transport protocols that are chosen according to transport preferences
set by locally on a per-message or per-node basis, and defaults to the remote node's preferences specified in a [[NodeAdvert#nodeadvert]] message.

##### Network Identity Store


The [[Network Identity Store#network-identity-store]] engine maintains a [[IdentityStore#identitystore|data store]] with [[IdentityRecord#identityrecord|records]]
that contain information associated with identities of engines, nodes, pub/sub topics, and domains.

The source of this information can be either local configuration
or advertisements received from other nodes via P2P protocols.

For each [[EngineIdentity#engineidentity]] it stores its local engine address, if applicable to the implementation.

For each [[NodeIdentity#nodeidentity]], it stores transport addresses in order of preference, measurements, trust value, and reputation value.

For each [[TopicIdentity#topicidentity]], it stores the [[PubSub#pubsub]] [[TopicAdvert#topicadvert]].

<div class="v2" markdown>


For each [[DomainIdentity#domainidentity]], it stores the [[DomainAdvert#domainadvert]].

</div>

#### Intra-domain protocols


--8<-- "networking/intra-domain.md:purpose"

#### PubSub


The [[PubSub#pubsub]] engine implements a P2P topic-based pub/sub protocol and performs inter-node multicast message routing within a domain.

#### Storage


The [[Storage#storage]] engine implements a P2P block storage protocol.

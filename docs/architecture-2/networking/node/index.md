---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Intra-node & inter-node protocols

## Purpose

<!-- --8<-- [start:purpose] -->
This group of engines are responsible for facilitating communication
between local engines (intra-node),
and between engines of two directly connected remote nodes (inter-node).

These engines provide message routing and network transport functionality,
and store information about network identities:
advertisements received from the network and associated local metadata.
<!-- --8<-- [end:purpose] -->

## Overview

### Router

#### Purpose

--8<-- "node/router/index.md:purpose"

#### Addressing

Nodes, pub/sub topics, and domains are addressed by their cryptographic identities.
Engine instance identities are derived from
the node identity the engine belongs to and an engine instance name
using a cryptographic hash function with an optional key.

Signed advertisement messages are used to bind addresses together from different layers:

- [[EngineAdvert]]: binds an engine name to a node ID and engine ID
- [[NodeAdvert]]: binds a node address to transport addresses
- [[DomainAdvert]]: binds a domain address to node addresses

The source address of an [[EngineMessage]] is always the [[EngineIdentity]] of an engine instance,
while its [[DestinationIdentity]] can belong to either an engine instance, pub/sub topic, or domain,
which corresponds to unicast, multicast, and anycast communication patterns, respectively.

A unicast message is sent between two (local or remote) engine instances,
a pub/sub message is sent from an engine instance to all subscribers of a topic.
while an anycast message is sent from an engine instance to any member of a domain,
Pub/sub messages are sent between local engine instances via the [[Router]]
that manages subscriptions and routes messages,
whereas inter-node pub/sub messages are handled by the [[PubSub]] engine.

When an [[EngineMessage]] is sent between peers,
either the source engine or the [[Router]] wraps it in a [[NodeMessage]].
The [[Router]] sends outgoing [[NodeMessage]]s to [[Transport]].
[[Transport]] then encapsulates the [[EngineMessage]] in a [[TransportMessage]]
and sends it off for delivery over the network to the transport plugin
that corresponds to the chosen [[TransportAddress]] of the peer.
The transport plugin then sends the [[EngineMessage]] as the payload of the respective transport protocol.

#### Routing

The Router makes routing decisions based on the [[DestinationIdentity]] of an [[EngineMessage]],
and forwards the message either to one or more local engines,
or to the [[Transport]] engine for delivery to a remote node.

The message processing and routing process is described in the [[EngineMessage]] section.

#### Inter-node messages

Inter-node messages are transmitted over authenticated and encrypted transport channels.

When forwarding an [[EngineMessage]] to a remote node,
the *Router* wraps it in [[NodeMessage]],
and forwards it to [[Transport]] for delivery over the network.

While upon reception of a [[NodeMessage]] from [[Transport]],
The [[Router]] unwraps the contained [[EngineMessage]] for delivery to its destination.

### Transport

#### Purpose

--8<-- "node/transport/index.md:purpose"

#### Connection pool

The *Transport* engine maintains a pool of connections to remote nodes,
which can be either permanent or ephemeral.
Ephemeral connections are disconnected after a period of inactivity,
and lost in case of a network error.
Permanent connections are maintained indefinitely and reconnected when the connection fails.

#### Transport protocols

The *Transport* engine delivers messages over the network via various transport protocol modules,
either using protocols directly over IP (such as QUIC or TLS),
through an overlay network (such as P2P, onion routed, or mix networks),
or via asynchronous, delay-tolerant networks.

Transport protocol modules are responsible for the authentication and encryption of each sent and received [[TransportMessage]],
but not responsible for authenticating or verifying the remote [[NodeIdentity]],
which is done by the [[Transport]] engine itself
via a [[ConnectionRequest]] upon establishing a connection.

Initially the QUIC-TLS [@quic-tls] and TLS 1.3 [@tls] protocols are supported for standalone nodes,
running over UDP and TCP, respectively.
As UDP may be blocked on 3-5% of networks [@quic-app],
offering both transport options
allows better connectivity for nodes on restricted networks.

Nodes that run inside browsers
may use either the WebTransport [@webtransport] or WebSocket [@websocket] protocols.
These allow HTTP connections to be upgraded to bidirectional streams over QUIC-TLS and TLS 1.3, respectively.

A [[TransportAddress]] contains all information necessary for a transport module to establish a connection,
including the long-term public key used by the transport protocol.
In case of TLS, which is used by all of the above protocols,
this is the public key of the self-signed X.509 certificate.
[[NodeAdvert]] messages contain one or more transport addresses to facilitate connection establishment.

### QUIC

QUIC [@quic] allows stream multiplexing with ordered, reliable delivery for each stream independently,
which reduces latency by removing head-of-line blocking across different streams.
QUIC also supports unreliable, unordered delivery via a protocol extension [@quic-unreliable].

When using reliable, ordered communication, a stream is created for each source-destination engine address pair.
Unreliable messages are useful for protocols such as multicast and gossip messages that do not require acknowledgement,
as these protocols handle resilience themselves.

QUIC has a modular architecture that allows the choice of security protocol.
The most common one is TLS [@quic-tls],
however, it has the drawback of using X.509 certificates,
which are unnecessary for decentralized networks
that do not rely on trusted Certificate Authorities (CA).
X.509 introduces additional complexity that may lead to security vulnerabilities,
and increases the size of the handshake message.

### Transport protocol and address selection

A signed [[NodeAdvert]] binds a node ID to one or more transport addresses.
In order to establish a connection, a [[NodeAdvert]] must be known by the local node.

When an outgoing message arrives at the [[Transport]] engine,
a transport protocol is chosen based on the transport constraints and requirements,
specified either in the outbound message headers,
or otherwise determined by per-node settings or defaults in the local configuration.
Given the chosen protocol(s), an appropriate transport address is chosen
from the addresses known for the destination node.
When a connection already exists that satisfies the transport constraints,
it is reused, otherwise a new connection is established to one of the known addresses.
When multiple suitable addresses are available,
the node's own address preferences are also taken into account,
expressed as a preference metric in the [[NodeAdvert]].

#### Transport preferences

Message ordering and reliability guarantees may vary per message,
an appropriate transport protocol is selected
according to transport constraints and requirements of each outgoing message.

Transport protocol choice is based on [[TransportPrefs|Transport preferences]]
that can be specified in either
an [[EngineMessage]] header,
or a [[NodeIdentityRecord]] stored by the [[Network Identity Store]] engine,
which contains both [[NodeAdvert]s received from the network
and local preferences associated with nodes.

When multiple transport addresses of a peer are known for the transport(s) chosen according to transport preferences,
then address choice is based on both the peer's own preferences in its [[NodeAdvert]],
and local measurements (e.g. latency) and preferences (e.g. prefer LAN over WAN IP addresses)

#### Connection establishement

To establish a connection, the Transport engine needs a [[TransportAddress]] to connect to,
which contains the transport protocol and address for the network connection.

In case of transports over IP that use X.509 certificates (such as QUIC or Secure WebSocket), the [[TransportAddress]] contains the destination IP address & port, as well as the certificate issuer's public key, which is used for subsequent verification of the remote peer's transport certificate.
Whereas for transports that use public key addressing, the destination public key address is given instead, possibly together with additional transport-specific dial information.

During connection establishment,
in order to ensure the security of the transport channel,
the initiator must verify the responder's transport public key,
which is known by the initiator since it is present in the [[NodeAdvert]].
Since node identities are separate from transport identities,
mutual authentication of node identities is necessary,
which happens right after establishing
an authenticated and encrypted transport channel,
using the [[ConnectionRequest]] message sent by the initiator of the connection.

TLS-based protocols offer 1-RTT and 0-RTT handshakes,
and use X.509 certificates to authenticate the server, and optionally the client.
Since 0-RTT is prone to replay attacks, it is not used,
neither are X.509 client certificates.

Once the connection is set up, Transport sends a [[PeerConnected]] notification,
or in case of connection failure a [[PeerConnectFailed]] notification instead.
While at the end of the connection, a [[PeerDisconnected]] notification is sent

### Message encoding

Message encoding (a.k.a. serialization and marshalling) is necessary before transmitting messages over the network.

Encoding and decoding of messages are done by the [[Transport]] engine
when sending and receiving messages.

The encoding format must satisfy the following requirements:

- Binary encoding and external schema: for fast parsing and compact message size.
- Versioning: to facilitate gradual protocol upgrades in a distributed system.
- Language and platform-agnostic: available for a variety of platforms and languages.
- Specification available.
- Simplicity: low complexity of specification and implementations.

The Binary Application Record Encoding (BARE) [@bare] format satisfies these requirements,
and is the recommended encoding for the system.

Protocol Buffers [@protobuf] is an alternative that provides suffient functionality
at the cost of higher complexity and less resilience.

Streaming protocols such, as QUIC and TLS,
necessitate message framing,
which also allows specifying the message encoding:
each message is prefixed with a header
that specifies the message length and encoding type.

### Network Identity Store

--8<-- "node/id-store/index.md:purpose"

## Message flow

<!-- Diagram illustrating message flows between engines -->

<figure class="invertable" markdown="span">

![Inter-node messages](node.dot.svg)

<!-- --8<-- [start:fig-node-caption] -->
<figcaption markdown="span">

**Unicast message** from engine *A_X* to engine *A_Y*, along edges labeled *Y*.
**Multicast message** from publisher engine *A_Z* to topic *T*, delivered to subscribed engines *A_X* and *A_Y* by the router *A_R*, along edges labeled *T*.

</figcaption>
<!-- --8<-- [end:fig-node-caption] -->

</figure>

<figure class="invertable wide" markdown="span">

![Unicast message](unicast.dot.svg)

<!-- --8<-- [start:fig-unicast-caption] -->
<figcaption markdown="span">

**Unicast message** between engine *A_X* of node *A* and engine *B_X* of node *B*,
via router engines *A_R* & *B_R* and transport engines *A_T* & *B_T*.

</figcaption>
<!-- --8<-- [end:fig-unicast-caption] -->

</figure>

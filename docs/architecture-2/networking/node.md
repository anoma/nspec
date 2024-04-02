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

--8<-- "node/router.md:purpose"

#### Addressing

Both the source and destination address of an [[EngineMessage#enginemessage]]
is an [[ExternalIdentity#externalidentity]].
The source is always the [[EngineIdentity#engineidentity]] of an engine instance,
while the [[DestinationIdentity#destinationidentity]] can belong to either an engine instance, a domain, or a pub/sub topic,
which corresponds to unicast, anycast, and multicast communication patterns, respectively.

A unicast message is sent between two (local or remote) engine instances,
an anycast message is sent from an engine instance to any member of a domain,
while a pub/sub message is sent from an engine instance to all subscribers of a topic.
Pub/sub messages are sent between local engine instances via the [[Router#router]]
that manages subscriptions and routes messages,
whereas inter-node pub/sub messages are handled by the [[PubSub#pubsub]] engine.

When an [[EngineMessage#enginemessage]] is sent between peers, it is wrapped in a [[P2PMessage#p2pmessage]] and signed by the source [[NodeIdentity#nodeidentity]].
The *node identity* is defined as the external identity of the [[Router#router]] engine instance of a node.

#### Routing

The Router makes routing decisions based on the [[DestinationIdentity#destinationidentity]] of an [[EngineMessage#enginemessage]],
and forwards the message either to one or more local engines,
or to the [[Transport#transport]] engine for delivery to a remote node.

The message processing and routing process is described in the [[EngineMessage#enginemessage]] section.

#### Inter-node messages

When forwarding an [[EngineMessage#enginemessage]] to a remote node,
the *Router* wraps it in [[P2PMessage#p2pmessage]],
signs it with its [[NodeIdentity#nodeidentity]] key,
and forwards it to [[Transport#transport]] for delivery over the network.

### Transport

#### Purpose

--8<-- "node/transport.md:purpose"

#### Connection pool

The *Transport* engine maintains a pool of connections to remote nodes,
which can be either permanent or ephemeral.
Ephemeral connections are disconnected after a period of inactivity,
and lost in case of a network error.
Permanent connections are maintained indefinitely and reconnected when the connection fails.

#### Transport protocols

The *Transport* engine delivers messages over the network via various transport protocols,
either using protocols directly over IP (such as QUIC or Secure WebSocket),
through an overlay network (such as onion routed or mix networks),
or via asynchronous, delay-tolerant networks.

Transport protocols are responsible for the authentication and encryption of each sent and received [[TransportMessage#transportmessage]],
but not responsible for authenticating or verifying remote [[NodeIdentity#nodeidentity|node identities]],
which is done by the [[Router#router]] instead,
by signing and verifying each sent and received [[P2PMessage#p2pmessage]].

#### Transport preferences

Transport protocol choice is based on [[TransportPrefs#transportprefs|Transport preferences]]
that can be specified in either
an [[EngineMessage#enginemessage]] header,
or a [[NodeIdentityRecord#nodeidentityrecord]] stored by the [[Network Identity Store#network-identity-store]] engine,
which contains both [[NodeAdvert#nodeadvert]]s received from the network
and local preferences associated with nodes.

When multiple transport addresses of a peer are known for the transport(s) chosen according to transport preferences,
then address choice is based on both the peer's own preferences in its [[NodeAdvert#nodeadvert]],
and local measurements (e.g. latency) and preferences (e.g. prefer LAN over WAN IP addresses)

#### Connection establishement

To establish a connection, the Transport engine needs a [[TransportAddress#transportaddress]] to connect to,
which contains the transport protocol and address for the network connection.

In case of transports over IP that use X.509 certificates (such as QUIC or Secure WebSocket), the [[TransportAddress#transportaddress]] contains the destination IP address & port, as well as the certificate issuer's public key, which is used for subsequent verification of the remote peer's transport certificate.
Whereas for transports that use public key addressing, the destination public key address is given instead, possibly together with additional transport-specific dial information.

Once the connection is set up, Transport sends a [[PeerConnected#peerconnected]] notification,
or in case of connection failure a [[PeerConnectFailed#peerconnectfailed]] notification instead.
While at the end of the connection, a [[PeerDisconnected#peerdisconnected]] notification is sent.

### Network Identity Store

--8<-- "node/id-store.md:purpose"

## Message flow

<!-- Diagram illustrating message flows between engines -->

<figure class="invertable">

![Inter-node messages](/nspec/images/node.dot.svg)

<!-- --8<-- [start:fig-node-caption] -->
<figcaption>

**Unicast message** from engine *A_X* to engine *A_Y*, along edges labeled *Y*.
**Multicast message** from publisher engine *A_Z* to topic *T*, delivered to subscribed engines *A_X* and *A_Y* by the router *A_R*, along edges labeled *T*.

</figcaption>
<!-- --8<-- [end:fig-node-caption] -->

</figure>

<figure class="invertable wide">

![Unicast message](/nspec/images/unicast.dot.svg)

<!-- --8<-- [start:fig-unicast-caption] -->
<figcaption>

**Unicast message** between engine *A_X* of node *A* and engine *B_X* of node *B*,
via router engines *A_R* & *B_R* and transport engines *A_T* & *B_T*.

</figcaption>
<!-- --8<-- [end:fig-unicast-caption] -->

</figure>

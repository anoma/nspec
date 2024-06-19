---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---


# P2P

```juvix hide
module architecture-2.engines.p2p;
```


## Network abstraction layer

The network abstraction layer is responsible for mapping logical sends (to a
topic and external identity) to physical sends (to physical addresses, e.g.
IPs). Higher protocol layers can send to and receive from external identities
and topics, subscribe to topics of interest, and unsubscribe from topics no
longer of interest. The network abstraction layer is responsible for keeping
relevant state, including who is interested in what topic, who is reachable at
what physical address, route information, latency information, and so forth.
Internally, the network abstraction layer handles peer discovery, sampling,
relaying, and routing, such that higher layers need only concern themselves with
messages destined for this agent. The network abstraction layer collects and
outputs latency information and relay accounting data which can be used to
inform higher-level decisions and tracking.

The network abstraction layer produces a logical pub/sub interface and consumes
a set of physical send/recv interfaces (e.g. UDP/IP, TCP/IP, etc.). The central
part we refer to as the _P2P intelligence engine_ (PIE), as it is expected to
run in parallel to higher layers and make decisions about discovery, routing,
etc. internally.

## Logical pub/sub interface

The logical pub/sub interface allows higher layers to send to and receive from
external identities and topics. All sends and receives reference an external
identity and a topic. In order to send a message to everyone, the "all" identity
can be used, and in order to send a message regardless of what topics have been
subscribed to, the sentinel empty string topic can be used (in other words, all
nodes are automatically subscribed to the default topic).

Topics are self-authenticating, in that only messages which satisfy the topic
predicate can be sent on the topic. Where we need to track strings for routing
tables, the content address of the function can be used. If nodes publish
invalid messages on the topic (which do not satisfy the predicates), other nodes
should refuse to relay those messages and ban the peers.

!!! note

    The difference between topics and external identities is that topics cannot be encrypted to. In the future (with witness encryption or similar) it may be possible to unify these concepts.

!!! todo

     Give examples for usecases at different points in the spectrum of Identity/Topic combinations.

!!! todo

     Simple local filtering on topics (i.e. subtopics) and potentially optimisations by broadcasting local filters.

```juvix
axiom Message : Type;
type Bool := True | False;
axiom ByteString : Type;

axiom ExternalIdentity : Type;
axiom Topic : Type;
axiom IO : Type;


axiom logicalSend : ExternalIdentity -> Topic -> Message -> IO;
axiom logicalOnRecv : (ExternalIdentity -> Topic -> Message -> IO) -> IO ;-- note: clarify notation for callback functions
axiom logicalSub : Topic -> IO ;
axiom logicalUnsub : Topic -> IO ;
```

## P2P intelligence engine (PIE 🥧)

The P2P intelligence engine (PIE) is where all the magic happens. The PIE
takes information from higher protocol layers, including entanglement and
bandwidth usage / routing preferences, and collects measurements internally
(latency, available routes) which are both used to inform decision-making,
allowing fine-grained tradeoffs between various constraints.

### Information from above

From above, PIE receives:

- Trust/entanglement information. For now this is assumed to be of the form of a
  scalar from 0 to 1 describing the entanglement between two external
  identities, such that 0 is unknown, 1 is completely trusted, and everything in
  between can be roughly understood as an interpolation.

- Routing preferences

    - Bandwidth usage preferences. For now this is just 1-bit of information,
      either "use any amount of bandwidth" or "minimise bandwidth".

    - Latency preferences. For now this is just 1-bit of information, either
      "minimize latency" or "don't care".

    - Cost preferences, with heterogeneous denominations

    - Trust/entanglement preferences for (intermediate) nodes
        - "avoid nodes with entanglement scores lower than X", for example

    - (eventually this can just be a function which selects between possible
      routes and PIE calls when it needs to decide)

### Information internally / from below

From below / internally, PIE collects:

- Relay accounting data (which other identities I have relayed how many / what
  size / bandwidth of messages for)

    - can start out very coarse (# of messages) and become more granular later
      if necessary

- Routing information (discovered from other nodes)

    - (external identity, physical address | external identity, latency) tuples

    - (external identity, {topics of interest}) tuples

    - includes latency information measured with local clock

    - can have multiple routes to the same destination w/different addresses,
      latency, etc.

    - nodes could express a priority list of their physical addresses

This information can be made available to higher protocol layers as desired.

### Decision-making

PIE makes decisions about how to route messages (from this agent to another
external identity and topic), and about when/how to relay messages destined for
another external identity and/or topic but sent initially to this agent.

### Sub-protocols

PIE includes sub-protocols for peer discovery, DHT (fallback routing option in
case local routing fails), trust-aware random peer sampling, trust-aware
relay/routing table synchronisation, NAT traversal/hole-punching, and possibly
collaborative filtering (in the future).

Sub-protocols:

- Peer discovery (e.g. via gossip/rps or DHT),

- DHT (SovKad)

- (Trust Aware) Random Peer Sampling

- (Trust Aware) Relaying Protocol

    - Nodes can request to not have their physical addresses forwarded, but
      instead relay packets via other nodes.

- (Trust Aware) Routing Table Sync

  - 1 bit of info instructing other node whether to share your (pubkey, IP) pair
    or share their IP in response to queries

  - Include latency data

 - NAT traversal / Hole Punching

 - Privacy-preserving interest discovery / collaborative filtering (incl. interesting bloom filter stuff)

### Routing notes

Logical routing should take into account compositionality of identities - e.g., if routes to Alice, Bob, and Charlie are known, but a route to (Alice && Bob && Charlie) is not, individual routes can be automatically tried. This state is constructed from physical address announcement messages sent (and signed) by particular external identities.

!!! todo

     Figure out details around implicit vs explicit domains and expected topologies under some reasonable assumptions.

!!! todo

     Figure out details around privacy-preservation in internal messages. Maybe the higher-layer should provide a default routing preference function which applies also to internal messages and can implement something like implicit domains (e.g. to restrict data leakage to a set of known nodes).

---

## Physical send/recv

Underlying physical networking layers are expected to expose an opaque type
`PhysicalAddress`, to which messages can be sent and from which they might be
received. Physical networking could be instantiated by a base physical protocol
such as TCP/IP or UDP/IP, or a more complex layered one such as Tor or a mixnet.
The physical layer needs to provide only two functions, `send` and `onRecv`,
which act as one would expect. Messages are assumed to be delivered either
completely or not at all, but the physical layer is not expected to provide any
form of authentication, ordering, or reliable delivery - those concerns are
handled by higher layers.

!!! todo

     Work remains to be done to integrate the privacy properties which might be provided by Tor or a mixnet into the privacy preferences and  trust graph, which the higher-level logical layers might be able to reason about. This will likely need to be an abstract model of their properties, to be used by the information flow control system.

```juvix
axiom PhysicalAddress : Type;
axiom send : PhysicalAddress -> ByteString -> IO;
axiom onRecv : (PhysicalAddress -> ByteString -> IO) -> IO;
```

Physical routing also requires an underlying state, but as existing stacks can
handle this perfectly well, so we keep all physical routing state and algorithms
out of scope of the Anoma protocols.

# Intra-domain P2P protocols

## Purpose

<!-- --8<-- [start:purpose] -->
This engine group implements intra-domain P2P protocols that run and offer services inside a domain.

Each domain has determines the set of protocols it runs
and the authentication mechanism it uses.
<!-- --8<-- [end:purpose] -->

## Overview

<div class="v2" markdown>


### Topology

The Topology engine is responsible for overlay topology and membership management of a domain.
The overlay maintenance protocol keeps the overlay connected despite high level of node failures.
The membership protocol provides a partial view of the online members known locally.

</div>

### PubSub

The PubSub engine is responsible for P2P topic-based publish-subscribe event dissemination.
It offers reliable causal delivery semantics with low latency.

#### Topics

Each topic has a [[TopicIdentity#topicidentity]], a set of publishers, and a set of subscribers.

Topics are advertised by [[TopicAdvert#topicadvert]] messages,
which include the [[TopicIdentity#topicidentity]], the set of publishers,
and an optional set of tags that allow automatic subscription to topics of interest.

Topic advertisements and events published in the topic
are authenticated by a signature of the [[TopicIdentity#topicidentity]].
Advertisements and events without a valid signature are dropped and not forwarded in the network.

#### Events

An *event* is a message sent to a topic by an authorized publisher.
An event may have causal dependencies, which need to be delivered beforehand.
The protocol includes a recovery mechanism for lost messages to ensure reliability,
which can be detected by either gaps in per-publisher sequence numbers,
or a missing dependency.

#### Usage

Engines access the pub/sub service via the [[Router#router]],
and do not directly talk to the [[PubSub#pubsub]] engine.

The [[PubSub#pubsub]] engine is solely responsible for participating in the P2P pub/sub protocols,
while the [[Router#router]] engine is solely responsible for providing a pub/sub service for local engines.

The PubSub engine subscribes to the local topics that correspond to the P2P pub/sub topics it manages.
This allows republishing received events locally, and publishing events of local origin to remote subscribers in the network.

The message flow diagram below shows intra-node and inter-node pub/sub messaging.

### Storage

The Storage engine provides P2P block storage.

It supports block put and get requests,
and a search mechanism to find nodes that store a specific storage block.

When a node receives a storage request,
it decides whether or not it provides service to the requesting node,
and for how long it can guarantee storage.
Storage nodes may require a certain level of trust and reputation,
some form of authentication, or a proof of payment
to store a block and guarantee its durability for a certain time.

Storage blocks have limited lifetime, and expired blocks are garbage collected.
Block lifetime may be extended upon request before expiration.
Durability guarantees are ensured by storage requests that include the desired length of time the block should be stored for,
and corresponding signed storage receipts with the provided guarantees.

## Message flow

<!-- Diagram illustrating message flows between engines -->

<figure class="invertable wide img-max">

![Multicast message](/nspec/images/multicast.dot.svg)

<!-- --8<-- [start:fig-multicast-caption] -->
<figcaption>

**Multicast (pub/sub) message** with publisher *A_X* and subscribers *B_X, C_X, D_X* sent to topic *T*.  
Published by node *A* and forwarded to node *B* and *C*, then from node *B* to node *D*.  
Multicast messages are sent along edges labeled *T*,  
while *B, C, D* are unicast messages between PubSub engine instances.

</figcaption>
<!-- --8<-- [end:fig-multicast-caption] -->

</figure>

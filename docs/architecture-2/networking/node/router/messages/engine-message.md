---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# EngineMessage

## Purpose

<!-- --8<-- [start:purpose] -->
A message sent between engine instances (both local & remote).
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[EngineMessageV1]]

--8<-- "../types/engine-message-v1.md:type"

**Triggers:**

[[EngineMessage]]

[[NodeMessage]]

[[RelayMessage]]

[[DomainRequest]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
When the router receives an *EngineMessage* from a local engine instance,
it processes it the following way:

1. It looks up `dst`, the [[DestinationIdentity]] in the routing table:

   - If not found, it sends a [[LookupIdentityRequest]]
     with the destination address to the [[Network Identity Store]] engine.
     - If the [[LookupIdentityResponse]] returns a result, it is added to the routing table,
       and the process continues with the next step.

2. If a route is found, the *EngineMessage* is processed the following way,
   depending on the type of [[DestinationIdentity]]:

   - Engine ([[EngineIdentity]]): unicast message to a local engine

     - The *Router* forwards the *EngineMessage* directly to the destination engine

   - Node ([[NodeIdentity]]): unicast message to a remote node

     - The *Router* wraps the *EngineMessage* in a [[NodeMessage]]
       with the *destination* set to the remote node's identity,
       then forwards it to the [[Transport]] engine for delivery over the network.

   - Topic ([[TopicIdentity]]): multicast message to a local pub/sub topic

     - The Router forwards the [[Message]] to all local engines subscribed to the multicast group,
       which might include the [[PubSub]] engine
       that is responsible for remote delivery over a P2P publish-subscribe protocol.

<div class="v2" markdown>

2. (cont.)

   - Relay ([[NodeIdentity]]): relayed message via another node

     - The *Router* wraps the *EngineMessage* in a [[RelayMessage]]
       with the *destination* set to the external identity from the routing table,
       the *source* set to the local node identity,
       and signs it with its identity key.
     - The *Router* then wraps the [[RelayMessage]] in a [[NodeMessage]]
       and sends it to [[Transport]] for delivery over the network.

   - Domain ([[DomainIdentity]]): anycast message to a domain

     - The *Router* wraps the *EngineMessage* in a [[DomainRequest]]
       with the destination set to the domain's identity and the *source* set to the local node identity.
     - The *Router* then sends the [[DomainRequest]] to the [[Domain Routing]] engine.

</div>

3. If no route is found, the message is dropped.

When processing the *EngineMessage*, the given [[RoutingPrefs]] and [[RoutingScope]] is respected.

!!! note

    The router subscribes to *[[IdentityUpdated]]* notifications of the [[Network Identity Store]] engine, in order to keep addresses in the routing table up to date.
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Transport -) Router: NodeMessage
Router -) Router: EngineMessage
Router -) Any Local Engine: EngineMessage
Any Local Engine -) Router: EngineMessage
Router -) Router: EngineMessage
Router -) Transport: NodeMessage
Router -) Router: RelayMessage
Router -) DomainRouting: DomainRequest
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

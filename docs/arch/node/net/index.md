# Network Subsystem

## Purpose

The *Network Subsystem* is responsible for
sending and receiving messages to and from remote nodes.

## Overview

The *Network Subsystem* consists of the following engines.

### [[Router]]

--8<-- "./router.juvix.md:purpose"

### [[Node Proxy]]

--8<-- "./node_proxy.juvix.md:purpose"

### [[Transport Connection]]

--8<-- "./transport_connection.juvix.md:purpose"

### [[Transport Protocol]]

<!--  --8<-- "./transport_protocol.juvix.md:purpose" -->

### [[Pub/Sub Topic]]

--8<-- "./pub_sub_topic.juvix.md:purpose"

### [[Storage]]

--8<-- "./storage.juvix.md:purpose"

## Diagrams

### Spawn tree & message flow

<figure markdown="span">

```mermaid
flowchart TD

N(Node)

E1(Engine1)
E2(Engine2)
E3(Engine3)

subgraph Network Subsystem
  R(Router)

  subgraph NodeProxies
    NP1(NProxy-1)
    NP2(NProxy-2)
    NP3(NProxy-3)
  end

  subgraph PubSub
    T1(Topic-1)
    T2(Topic-2)
    T3(Topic-3)
  end

  subgraph Transport
    TP1(TProto-1)
    TP2(TProto-2)
    TP3(TProto-3)

    TC11(TConn-1-1)
    TC12(TConn-1-2)
    TC21(TConn-2-1)
    TC31(TConn-3-1)
    TC32(TConn-3-2)
  end
end

NET(Network)

%% Spawn tree

N -.-> R & TP1 & TP2 & TP3 & E1 & E2 & E3
R -.-> NP1 & NP2 & NP3 & T1 & T2 & T3
TP1 -.-> TC11 & TC12
TP2 -.-> TC21
TP3 -.-> TC31 & TC32

%% Message flow

%% Intra-node communacation between local engines
E1 -- Send --> E2

%% First message via R to open a connection
E2 -- NodeSend --> R -- Send --> NP2 -- Send --> TP2 -- Send --> TC21 --> NET
E2 -- TopicForward --> R -- Forward --> T1

%% Subsequent messages
E2 -- Send --> NP2
E2 -- Forward --> T1

T1 -- Send --> E3
T1 -- Send --> NP1 -- Send --> TP1 -- Send --> TC12 --> NET
```
<figcaption markdown="span">

Spawn tree & message flow:
- dotted: spawn
- solid: message send

</figcaption>

</figure>
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

### [[Transport]]

--8<-- "./transport.juvix.md:purpose"

### [[Topic]]

--8<-- "./topic.juvix.md:purpose"

### [[Storage]]

--8<-- "./storage.juvix.md:purpose"

## Diagrams

### Spawn tree & message flow

```mermaid
flowchart TD

E1(Engine1)
E2(Engine2)
E3(Engine3)

R(Router)

NP1(NodeProxy1)
NP2(NodeProxy2)
NP3(NodeProxy3)

T1(Topic1)
T2(Topic2)
T3(Topic3)

T(Transport)
TP1(TransProto1)
TP2(TransProto2)
TP3(TransProto3)
TC1(TransConn1)
TC2(TransConn2)
TC3(TransConn3)

%% Spawn tree

R -.-> NP1
R -.-> NP2
R -.-> NP3

T -.-> TP1
T -.-> TP2
T -.-> TP3

TP1 -.-> TC1
TP1 -.-> TC2

TP2 -.-> TC3

TP3 -.-> TC4
TP3 -.-> TC5

%% Message flow

E1 -- EngineMsg --> R -- EngineMsg --> E2

%% First message to open a connection
A_E2 -- SendMsg --> A_R -- SendMsg --> A_NP1 -- SendMsg --> A_T -- SendMsg --> A_TP1 -- SendMsg --> A_TC1 -- NodeMsg --> B_TC3

%% Subsequent messages
A_E2 -- SendMsg --> A_NP1 -- SendMsg --> A_TC1 -- NodeMsg --> B_TC3
```

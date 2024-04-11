---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# RoutingTableDest

## Purpose

Destination of a [[RoutingTable#routingtable]] entry.

## Type

*Enum* with the following possible values.

| Value     | Type                                        | Description                                       |
|-----------|---------------------------------------------|---------------------------------------------------|
| Engine    | *[[EngineAddr#EngineAddr]]*                 | Local engine reachable directly                   |
| Topic     | *[[RoutingTableTopic#routingtabletopic]]*   | Locally subscribed engines to a topic             |
| Transport |                                             | Remote peer reachable via [[Transport#transport]] |
| Peer      | *[[NodeIdentity#nodeidentity]]*                         | Relay via remote peer                             |
| Domain    | *[[RoutingTableDomain#routingtabledomain]]* | Known domain members for sending requests to      |

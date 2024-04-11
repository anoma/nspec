---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# RoutingTableTopic

## Purpose

A pub/sub topic in a routing table entry.

## Type

*Struct* with the following fields.

| Field         | Type                           | Description                |
|---------------|--------------------------------|----------------------------|
| `creator`     | *[[EngineIdentity#engineidentity]]*        | Topic creator engine       |
| `subscribers` | *Vec\<[[EngineIdentity#engineidentity]]\>* | List of subscribed engines |

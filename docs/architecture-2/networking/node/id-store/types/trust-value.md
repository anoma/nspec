---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TrustValue

## Purpose

Express trust for a peer.

## Type

*u8*

## Values

- Range: `0..255`
- Notable values:
  - `0`: no trust, banned from communication
  - `128`: default value
  - `255`: fully trusted nodes (e.g. other nodes of the same user/entity)

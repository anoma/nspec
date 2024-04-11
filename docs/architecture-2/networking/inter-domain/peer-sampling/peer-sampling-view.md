---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# PeerSamplingView

## Purpose

Peer Sampling view exchange.

## Reception

- PeerSampling $\to$ [[PeerSamplingView#peersamplingview]] $\to$ PeerSampling

## Structure

| Field  | Type                | Description |
|--------|---------------------|-------------|
| `view` | *Vec\<NodeAdvert\>* | View        |

## Triggers

- PeerSampling $\to$ [[PeerSamplingView#peersamplingview]] $\to$ PeerSampling

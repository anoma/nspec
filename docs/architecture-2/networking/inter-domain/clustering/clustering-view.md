---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ClusteringView

## Purpose

Clustering view exchange.

## Reception

- Clustering $\to$ [[PeerSamplingView#peersamplingview]] $\to$ Clustering

## Structure

| Field  | Type                | Description |
|--------|---------------------|-------------|
| `view` | *Vec\<NodeAdvert\>* | View        |

## Triggers

- Clustering $\to$ [[PeerSamplingView#peersamplingview]] $\to$ Clustering

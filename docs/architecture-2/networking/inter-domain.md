---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Inter-domain P2P protocols

## Purpose

Inter-domain P2P protocols are responsible for peer sampling and clustering,
as well as routing requests to domains.

## Background

## Scope

## Functionality

### Peer Sampling

The [[Peer Sampling#peer-sampling]] engine runs a P2P gossip-based trust-aware peer sampling protocol
that provides a continously changing partial view of the network.

Nodes periodically exchange their partial views with each other, and update their local view after each exchange.
Peer sampling protocols are prone to attacks where partial views can be biased by attackers,
to prevent this and make the protocol more robust and avoid attacks,
nodes peform statistical analysis to filter out over-represented nodes in view exchanges,
and they always keep a number of trusted nodes in their view.

### Clustering

The clustering protocol performs node clustering according to a proximity metric based on shared domain membership.
When choosing gossip targets, it considers nodes from the Peer Sampling view.

Clustering optimizes the overlay structure by reducing the number of links necessary in the overlay by discovering nodes
that can exchange messages for multiple domains over a single connection.

### Domain Routing

The Domain Routing protocol allows routing join and data requests to one of the members of a domain,
via the small world overlay structure created by the Clustering protocol.

<!-- Outline the responsibilities of the engines and describe high-level protocols. -->

## Overview

<!-- High-level overview of the engines: introduce the engines, along with visualizations to illustrate their relationship. -->

## Communication diagram

<!-- Diagram illustrating message flows between engines -->

## Example scenario

<!-- Short message cascade from a typical common message sent to the machine  -->
<!-- E.g. an example of the common case "life of a transaction or whatever" flow from inputs to outputs -->

## Further reading


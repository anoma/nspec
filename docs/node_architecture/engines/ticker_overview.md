---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- ticker
- engine-overview
---

# `Ticker` Engine Family Overview

--8<-- "./docs/node_architecture/engines/ticker.juvix.md:ticker-engine-family"

The Ticker engine family provides a simple counter functionality, allowing
clients to increment a counter and retrieve its current value.

## Purpose

A ticker engine maintains a counter in its local state. It increases the counter
when it receives an `Increment` message and provides the updated result upon
receiving a `Count` message. The initial state initializes the counter.

## Engine Components

- [[Ticker Engine Messages|`Ticker` Engine Messages]]
- [[Ticker Engine Environment|`Ticker` Engine Environment]]
- [[Ticker Engine Dynamics|`Ticker` Engine Dynamics]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

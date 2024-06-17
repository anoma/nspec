---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# EngineIdentity

## Purpose

Identity of an engine.

## Type

*[[Digest]]*

## Value

A keyed or plain hash digest of the [[NodeIdentity]] and the engine instance name that is unique per node.

$$ H(NodeIdentity || EngineName) $$

Identities of the [[Router]] and [[Transport]] engines are not keyed and have well-known names to be always addressable.

## See also

- [[EngineAdvert]]

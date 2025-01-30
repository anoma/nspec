---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - types
  - prelude
  - index
---

# Types

```juvix
module arch.node.types;

import arch.node.types.basics open public;
import arch.node.types.crypto open public;
import arch.node.types.identities open public;
import arch.node.types.messages open public;

import arch.node.types.anoma open public;
import arch.node.types.engine open public;

{- Engine-specific types -}
import arch.node.types.transport open public;
import arch.node.types.storage open public;
import arch.node.types.router open public;
```

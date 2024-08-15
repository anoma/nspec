---
icon: octicons/container-24
search:
  exclude: false
tags:
  - engine-family
  - example
  - ticker
---

```juvix
module node_architecture.engines.ticker_protocol_types;

import node_architecture.engines.ticker_environment open;

import prelude open;
import node_architecture.types.engine_family as EngineFamily;
open EngineFamily using {
    Engine;
    EngineEnvironment;
    EngineFamily;
    mkActionInput;
    mkEngine;
    mkEngineEnvironment;
    mkEngineFamily
};
open EngineFamily.EngineEnvironment;

--- in a perfect world, the following would be in an engine family page of its own

type TickerClientMessage :=
  | Counter Nat;

TickerClientEnvironment : Type :=
  EngineFamily.EngineEnvironment
    Unit
    TickerClientMessage
    Unit
    Unit;

type TickerProtocolEnvironment :=
 | TickerEnv TickerEnvironment
 | ClientEnv TickerClientEnvironment
;

type TickerProtocolMessage :=
 | TickerMsg TickerMessage
 | TickerClientMsg TickerClientMessage;
```
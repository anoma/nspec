---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engines
- conventions
---

```juvix
module node_architecture.engines.ticker;
  import prelude open;
  import node_architecture.engines.ticker_overview open public;
  import node_architecture.engines.ticker_environment open public;
  import node_architecture.engines.ticker_dynamics open public;

    import node_architecture.types.engine_family as EngineFamily;
      open EngineFamily using {
          Engine;
          EngineEnvironment;
          EngineFamily;
          mkEngine;
          mkEngineEnvironment;
          mkEngineFamily
      };
    open EngineFamily.EngineEnvironment;
    import node_architecture.engines.ticker_environment open public;
    import node_architecture.engines.ticker_dynamics open public;

    EngineFamilyType : Type :=
      EngineFamily
        TickerLocalState
        TickerMsg
        TickerMailboxState
        TickerTimerHandle
        Unit
        Unit
        Unit 
        Unit;
```

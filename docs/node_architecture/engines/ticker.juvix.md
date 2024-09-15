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
          EngineFamily;
          mkEngineFamily
      };
    open EngineFamily.EngineEnvironment;
    import node_architecture.engines.ticker_environment open public;
    import node_architecture.engines.ticker_dynamics open public;
```

# Ticker engine family Type


<!-- --8<-- [start:ticker-engine-family] -->
```juvix
TickerEngineFamily : 
  EngineFamily
    TickerLocalState
    TickerMsg
    TickerMailboxState
    TickerTimerHandle
    TickerMatchableArgument
    TickerActionLabel
    TickerPrecomputation
  := mkEngineFamily@{
    guards := [incrementGuard ; countGuard];
    action := tickerAction;
    conflictSolver := \{ _ := [] }
  }
  ;
```
<!-- --8<-- [end:ticker-engine-family] -->



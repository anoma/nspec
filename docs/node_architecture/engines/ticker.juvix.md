---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engines
- conventions
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.ticker;
      import prelude open;
      import node_architecture.types.engine_family as Anoma;

      import node_architecture.engines.ticker_overview open public;
      import node_architecture.engines.ticker_environment open public;
      import node_architecture.engines.ticker_dynamics open public;
    ```

# Ticker engine family type

<!-- --8<-- [start:ticker-engine-family] -->
```juvix
TickerEngineFamily :
  Anoma.EngineFamily
    TickerLocalState
    TickerMailboxState
    TickerTimerHandle
    TickerMatchableArgument
    TickerActionLabel
    TickerPrecomputation
  := Anoma.mkEngineFamily@{
    guards := [incrementGuard ; countGuard];
    action := tickerAction;
    conflictSolver := tickerConflictSolver;
  }
  ;
```
<!-- --8<-- [end:ticker-engine-family] -->



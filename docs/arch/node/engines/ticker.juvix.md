---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engines
- conventions
---

??? note "Juvix preamble"

    ```juvix
    module arch.node.engines.ticker;
      import prelude open;
      import arch.node.types.engine_family as Anoma;

      import arch.node.engines.ticker_overview open public;
      import arch.node.engines.ticker_environment open public;
      import arch.node.engines.ticker_dynamics open public;
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



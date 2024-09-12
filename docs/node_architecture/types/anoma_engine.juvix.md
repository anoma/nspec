---
icon: octicons/gear-16
search:
exclude: false
tags:
  - engine-family
  - Juvix
---

??? info "Juvix imports"

    ```juvix
    module node_architecture.engines.types.anoma_engine;
    import node_architecture.engines.ticker open;
    ```

## Anoma Engine Families in Juvix

```juvix
type EngineFamily :=
  | EngineFamilyTicker TickerEngineFamily
  ;
```
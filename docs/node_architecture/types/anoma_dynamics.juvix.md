---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.anoma_dynamics;
    -- import node_architecture.engines.ticker_dynamics open using {TickerDynamics};
    ```

# Anoma Engine Dynamics

```
type AnomaDynamics :=
  | TickerDynamics TickerDynamics
```

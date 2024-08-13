---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.engines.types.anoma_dynamics;
      import tutorial.engines.examples.ticker_dynamics open;
    ```

# Anoma Engine Dynamics

```
type AnomaDynamics :=
  | TickerDynamics TickerDynamics
```

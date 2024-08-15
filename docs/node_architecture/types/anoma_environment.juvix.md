---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.anoma_environment;
      import node_architecture.engines.ticker_environment open;
    ```

# Anoma Engine Environments

```juvix
type AnomaEnvironment :=
  | TickerEnv TickerEnvironment
```

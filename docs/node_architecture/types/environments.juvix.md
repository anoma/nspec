---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.engines.types.environments;
      import tutorial.engines.examples.ticker_environment open;
    ```

# Anoma Engine Environments

```juvix
type AnomaEnvironment :=
  | TickerEnv TickerEnvironment
```

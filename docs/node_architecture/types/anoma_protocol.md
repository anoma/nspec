---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.engines.anoma_protocol;
      import tutorial.engines.examples.ticker_protocol_types open;
    ```

# Anoma Engine Protocol Types

```juvix
type AnomaEngineProtocolEnvironment :=
  | TickerProtocolEnv TickerProtocolEnvironment;

type AnomaEngineProtocolMessage :=
  | TickerProtocolMsg TickerProtocolMessage;
```
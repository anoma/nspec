---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.engines.protocol_types;
      import tutorial.engines.examples.ticker_protocol_types open;
    ```

# Anoma Engine Protocol Types

```juvix
type AnomaEngineProtocol :=
  | TickerProtocol TickerProtocolEnvironment TickerProtocolMessage
```
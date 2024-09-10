---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.anoma_protocol;
      import node_architecture.engines.ticker_protocol_types open;
    ```

# Anoma Engine Protocol Types

```juvix
type AnomaEngineProtocolMessage :=
  | TickerProtocol TickerProtocolEnvironment TickerProtocolMessage
```
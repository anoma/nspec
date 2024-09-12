---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Engine-Family
- Engine-Instances
- Juvix
---



??? info "Juvix preamble"

    ```juvix
    module node_architecture.types.anoma_message;
    import node_architecture.basics open;
    import node_architecture.engines.ticker_overview as Ticker;
    ```

# Anoma Messages

```juvix
type AnomaMessage :=
  | TickerMsg Ticker.Msg
```
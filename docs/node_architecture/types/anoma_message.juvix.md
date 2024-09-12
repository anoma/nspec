---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Anoma-Message
- Juvix
---

??? info "Juvix preamble"

    ```juvix
    module node_architecture.types.anoma_message;
    import node_architecture.basics open;
    import node_architecture.engines.ticker_overview open using {TickerMsg}
    ```

# Anoma Messages

```juvix
type Msg :=
  | MsgTicker TickerMsg
  ;
```
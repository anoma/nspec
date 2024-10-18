---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Anoma-Message
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.anoma_message;
    import node_architecture.engines.ticker_messages open;
    ```

# Anoma Messages

An _Anoma_ message is a admissible messages that can be sent between nodes in
the network. An Anoma message is of the type `Msg`. Each constructor of the type
`Msg` corresponds to a specific type of message comming from a specific engine
family. For example, the engine family `Ticker` has a corresponding message type
`TickerMsg`.

```juvix
type Msg :=
  | MsgTicker TickerMsg
  ;
```

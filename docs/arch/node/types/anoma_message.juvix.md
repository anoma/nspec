---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Anoma-Message
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.anoma_message;
    import arch.node.engines.ticker_messages open using {TickerMsg};
    ```

# Anoma Messages

An _Anoma_ message is a admissible messages
that can be sent between nodes in the network.
An Anoma message is of the type `Msg`.
Each constructor of the type `Msg`
corresponds to a specific type of message comming from a specific engine.
For example, the engine `TickerEngine`
has a corresponding message type `TickerMsg`.

<!-- --8<-- [start:anoma-messages-type] -->
```juvix
type Msg :=
  | MsgTicker TickerMsg
  ;
```
<!-- --8<-- [end:anoma-messages-type] -->
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

An _Anoma_ engine environment is a collection of all the necessary
information/context that an engine instance needs to operate.
See [[Engine Environments]] for more information on engine environments.
Below is the definition of the type `Env` which represents an Anoma engine
environment. This means, an Anoma engine instance would have an environment of
type `Env`. 

For example, an environment for an engine instance of the engine family `Ticker`
is of type `TickerEnvironment`.

```juvix
type Env :=
  | EnvTicker TickerEnvironment
```

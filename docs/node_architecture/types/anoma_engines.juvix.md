---
icon: octicons/gear-16
search:
exclude: false
tags:
  - engine-family
  - Juvix
---


??? info "Juvix imports"

    ```juvix
    module node_architecture.engines.types.anoma_engines;

    import node_architecture.basics open;
    import node_architecture.types.environments open;
    import node_architecture.types.dynamics open;
    import node_architecture.types.protocol_types open;
    import node_architecture.types.engine_family as Base open using {EngineFamily};
    -- import tutorial.engines.ticker as Ticker open using {TickerFamily; zeroTicker};
    ```

## Anoma Engine Families in Juvix

Below, we use [Juvix](https://docs.juvix.org) to define a sum type to
index the different engine families.

```juvix
type AnomaEngineFamilyType :=
  | Ticker
  ;
```

Using the name of the engine family, we can fine all the Juvix modules related to the engine family.
For example, the `X` engine family is defined in the `node_architecture.engines.X` module.

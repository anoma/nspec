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
    module architecture-2.engines.index;

    import architecture-2.Prelude open;
    import architecture-2.types.EngineFamily as Base open using {EngineFamily};

    import tutorial.engines.Ticker as Ticker open using {TickerFamily; zeroTicker};
    ```

# Anoma Engine Families

In Anoma, an **engine** represents a computational process characterised by its
state and behaviors. These engines are defined through _guarded actions_
within an execution context known as the _engine environment_ of the engine
instance. For a more detailed explanation, please refer to the section on
[[Engines in Anoma|Engine in Anoma's tutorial]].

The Anoma Specification is structured around various _engine families_. Each of
these families are designed to perform specific tasks within the system, such as handling
a particular consensus operation. Members of this family are individual engine
instances that share the same behavior but have different local states and
names.

## Engine Families

Below, we use [Juvix](https://docs.juvix.org) to define a type
where each type constructor represent a corresponding engine family.

```juvix
type AnomaEngineFamily :=
  | TickerEngineFamily (Box _ TickerFamily)
  ;
```

!!! warning

  Please be aware that the definition of `AnomeEngineEnv` is not yet final.
  We are continually expanding the Juvix part of the specification with new engine families.

As an example of an engine instane, we have the canonical ticker. 

```juvix
tickerInstance : AnomaEngineFamily :=
  TickerEngineFamily (Ticker.EngineFamilyType , zeroTicker);
```


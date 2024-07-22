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

    !!! note 

        This module is not intended to be translated to Isabelle, as it contains
        unsopported definitions. It is used to provide a high-level overview of the
        engine families used.

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

??? quote "Boxing types in Juvix" 

    To list all possible engine families, we use the `Box` type constructor to
    define a sum type. So **Box A a** is a type-valued function that encapsulates
    a type along with a term of that type. It is used to group together the type
    information and its corresponding value within a single entity.


    ```juvix
    Box (A : Type) (a : A) : Type := Pair Type A;
    ```

    For example, 
      
    ```
    fourty-two : Type := Box Nat 42;
    ```

    !!! todo
        
        The `Box` definition should go in the prelude once the Juvix translation to Isabelle
        supports this kind of type definition.

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


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
    module node_architecture.engines.index;

    import node_architecture.basics open;
    import node_architecture.types.environments open;
    import node_architecture.types.dynamics open;
    import node_architecture.types.protocol_types open;
    import node_architecture.types.engine_family as Base open using {EngineFamily};

    ```

    !!! todo  "fix code in this page"

        import tutorial.engines.ticker as Ticker open using {TickerFamily; zeroTicker};


    !!! note

        This module is not intended to be translated to Isabelle, as it contains
        unsupported definitions. It is used to provide a high-level overview of the
        engine families defined in Juvix used in the specification.

# Anoma Engine Families

In Anoma, an **engine** represents a computational process characterised by its
state and behaviors. These engines are defined through _guarded actions_
within an execution context known as the _engine environment_ of the engine
instance. For a more detailed explanation, please refer to the tutorial on
[[Engines in Anoma]].

The Anoma Specification is structured around various _engine families_. Each of
these families are designed to perform specific tasks within the system, such as handling
a particular consensus operation. Members of this family are individual engine
instances that share the same behavior but have different local states and
names.

Thus, an engine family
is a pair of an engine environment type
and a set of guarded actions;
the additional context of this definition
are protocol-level types for messages and environments.

<!--
## Engine Families in Juvix

Below, we use [Juvix](https://docs.juvix.org) to define a sum type to
index the different engine families.

!!! warning

  Please be aware that the definition of `AnomaEngineFamily` below is not yet final.
  For the time being, we are using the `Ticker` engine family as an example.
  We are continually expanding the Juvix part of the specification with new engine families.

```juvix
type AnomaEngineFamilyType :=
  | Ticker
  ;
```

## Engine Family Getters

Getters help retrieve types for specific engine families:

```
getEngineFamilyType (fam : AnomaEngineFamilyType) : Type :=
  case fam of {
  | Ticker := Ticker.EngineFamilyType
   };
```

```
getEngineInstanceType (fam : AnomaEngineFamilyType) : Type :=
  case fam of {
  | Ticker := Ticker.EngineInstanceType
   };
```

```
getEnvironmentType (fam : AnomaEngineFamilyType) : Type :=
  case fam of {
  | Ticker := Ticker.EnvType
   };
```

```
getGuardedActionType (fam : AnomaEngineFamilyType) : Type :=
  case fam of {
  | Ticker := Ticker.GuardedActionType
   };
```

## Engine Families in Juvix

While engine families provide a framework, in practice, we work with instances
of these engine families. Below, we define another union type to index engine
instances. Again, we use the Ticker engine family as an example. To list all
possible engine families, we use the Box type constructor to define a sum type.

??? quote "Auxiliary box types in Juvix"

    To list all possible engine families, we use the `Box` type constructor to
    define a sum type. So **Box A a** is a type-valued function that encapsulates
    a type along with a term of that type. It is used to group together the type
    information and its corresponding value within a single entity.

    ```
    Box (A : Type) (a : A) : Type := Pair Type A;
    ```

    For example,

    ```
    fourty-two : Type := Box Nat 42;
    ```

Then:

```
type AnomaEngineInstanceType :=
  | TickerInstance (Box Ticker.EngineInstanceType Ticker.TickerFamily)
  ;
```

As an example of an engine instance, we have the canonical ticker.

```
tickerInstance : getEngineInstanceType Ticker := zeroTicker;
```

-->

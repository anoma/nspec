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

    import Stdlib.Prelude as Prelude;
    
    import architecture-2.engines.basic-types open;
    import architecture-2.engines.base as Base;
    open Base using {EngineFamily};

    import tutorial.engines.Ticker as Ticker;
    ```

# Anoma Engine Families

In Anoma, an **engine** represents a computational process characterised by its
state and behaviors. These engines are defined through _guarded actions_
within an execution context known as the _local environment_ of the engine
instance. For a more detailed explanation, please refer to the section on
[[Engines in Anoma|Engine in Anoma's tutorial]].

The Anoma Specification is articulated around various _engine families_. Each of
these families are designed to perform specific tasks within the system, such as handling
a particular consensus operation, and each family consists of multiple **engine instances**.
While all engine instance initally share the same behavior,
each engine instance is different in their (local) state and their name, data 
part of the engine's execution environment, and therefore, their purpose.

## Local Environments

Below, we use [Juvix](https://docs.juvix.org) to define `AnomeEngineEnv`, the type for
local environments used by each engine family in Anoma. 

By examining these local environments, we can identify the engine families
currently considered in Anoma. These local environments essentially provide the
execution context for their respective engines. So, remember, each type
constructor of `AnomeEngineEnv` represents the local environment for a distinct
engine family.

```juvix
type AnomaEngineEnv := 
  | EngineFamilyEnv Ticker.EngineEnvironment
  ;
```

!!! warning 

  Please be aware that the definition of `AnomeEngineEnv` is not yet finalised. 
  We are continually expanding the Juvix part of the specification with new engine families.



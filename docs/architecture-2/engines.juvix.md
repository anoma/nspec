---
icon: octicons/gear-16
search:
exclude: false
tags:
- engine
- mailbox
- engine-type
- Juvix
---


!!! warning

    This document is a work in progress. Please do not review it yet.
    Also, this file should be probably somewhere else, like in the architecture-2 folder.


??? info "Juvix imports"

    ```juvix
    module architecture-2.engines;

    import Stdlib.Prelude as Prelude;
    
    import architecture-2.engines.basic-types open;
    import architecture-2.engines.base open;

    import tutorial.engines.engine-template-example open;
    ```

# Engines

Anoma's implementation consists of various _engines_. An _engine_ is a computational process within a trusted domain, characterised as a function parameterised over state, input message, and output message types. More details can be found in the [[Engine in Anoma|Engine in Anoma's tutorial]].

## Anoma Engine Types Compendium

### Engine-Related Types

All admissible  types are listed in a union/coproduct type called `AnomaEngine`, serving two main purposes:

- **Type Discovery**: Identifies all permissible engine types.

- **Convenience**: Simplifies writing state transition functions for guarded actions.

Mapping from engine labels to their actual types, and providing functions to retrieve the local state type and message type for each engine, given the engine label.

```juvix
type AnomaEngine :=
  | EngineAuctioneer
  ;
```

Getter functions:
```juvix
getEngineTypes (e : AnomaEngine) : Type :=
  case e of {
    | EngineAuctioneer := (AuctioneerLocalStateType , AuctioneerMessageType)
    };

getEngineLocalStateType (e : AnomaEngine) : Type :=
  fst (getEngineTypes e);

getEngineMessageType (e : AnomaEngine) : Type :=
  snd (getEngineTypes e)

getEngineType (e : AnomaEngine) : Type :=
  EngineType
    (getEngineLocalStateType e) 
    (getEngineMessageType e);
```

Similarly, list all possible local states of engines as coproducts to use this type when spawning new engine instances:

```juvix
type AnomaEngineLocalState :=
    | LocalStateAuctioneer AuctioneerLocalStateType
    ;
```
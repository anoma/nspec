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


??? info "Juvix imports"

    ```juvix
    module architecture-2.engines;

    import Stdlib.Prelude as Prelude;
    
    import architecture-2.engines.basic-types open;
    import architecture-2.engines.base as Base;
    open Base using {Engine};

    import tutorial.engines.Auctioneer as Auctioneer;
    ```

# Engines

Anoma's implementation consists of various _engines_. An _engine_ is a computational process within a trusted domain, characterised as a function parameterised over state, input message, and output message types. More details can be found in the [[Engine in Anoma|Engine in Anoma's tutorial]].


All admissible  types are listed in a union/coproduct type called `AnomaEngine.
Each constructor of the coproduct type corresponds to a different engine type.
We only keep the local environment for each Engine as it's only the data needed
to spawn a new engine instance.

```juvix
type AnomaEngine :=
  | EngineAuctioneer Auctioneer.LocalEnvironment
  -- | EngineConsensus Consensus.LocalEnvironment
  ;
```

```juvix
getLocalStateType (e : AnomaEngine) : Type :=
  case e of {
  | (EngineAuctioneer _) := Auctioneer.LocalStateType
  }
  ; 
```
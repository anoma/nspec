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

Anoma's implementation consists of various _engines_ family. 
Each family serves on specific purpose such as ordering and consensus tasks.
At the core, an _engine_ is a computational process with local state and behaviour defined via guarded actions. More details can be found in the [[Engine in Anoma|Engine in Anoma's tutorial]].

All admissible engine families can be discovered by looking at the
data constructors in the type `AnomeEngineEnv` defined below.
Each constructor of the coproduct type is in correspondance to a different engine family.

```juvix
type AnomaEngineEnv :=
  | FamilyAuctioneer Auctioneer.LocalEnvironment
  -- | EngineConsensus Consensus.LocalEnvironment
  ;
```

```juvix
getLocalStateType (e : AnomaEngineEnv) : Type :=
  case e of {
  | (FamilyAuctioneer _) := Auctioneer.LocalStateType
  }
  ; 
```
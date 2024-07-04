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

# Engine Families

Anoma's implementation consists of various _engines_ families.
Each family serves a specific purpose, such as consensus tasks.
At its core, an _engine_ is a computational process with local state and behaviour defined via guarded actions. More details can be found in the [[Engine in Anoma|Engine in Anoma's tutorial]].

Now, all admissible engine families can be discovered by examining the data constructors in the type `AnomeEngineEnv` defined below. Each constructor of this coproduct type corresponds to a different engine family.

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
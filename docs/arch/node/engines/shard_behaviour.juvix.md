---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-behaviour
- juvix-module
tags:
- shard
- execution
- engine-behavior
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.shard_behaviour;
    import prelude open;
    import arch.node.engines.shard_messages open;
    import arch.node.engines.shard_environment open;
    import arch.node.types.anoma_message open;
    import arch.node.types.engine_behaviour open;
    import arch.node.types.engine_environment open;
    import arch.node.types.messages open;
    ```

# Shard Behaviour
!!! todo
    Figure out what a ``behaviour'' is, and write one for the shard
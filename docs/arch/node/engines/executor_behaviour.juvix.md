---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-behaviour
- juvix-module
tags:
- execution
- executor
- engine-behavior
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.executor_behaviour;
    import prelude open;
    import arch.node.engines.executor_messages open;
    import arch.node.engines.executor_environment open;
    import arch.node.types.anoma_message open;
    import arch.node.types.engine_behaviour open;
    import arch.node.types.engine_environment open;
    import arch.node.types.messages open;
    ```

# Executor Behaviour
!!! todo
    Figure out what a ``behaviour'' is, and write one for the executor
---
icon: octicons/gear-24
search:
  exclude: false
tags:
- engines
- conventions
---

??? quote "Juvix preamble"

    ```juvix
    module arch.node.net.router;

    import prelude open;
    import arch.node.net.router_messages open;
    -- import arch.node.net.router_environment open;
    -- import arch.node.net.router_behaviour open;
    import arch.node.types.engine open;
    open template_environment_example;
    ```

# Router Engine

## Purpose

--8<-- [start:purpose]
The *Router* engine is responsible for
spawning a [[Node Proxy]] instances for each remote node,
and a [[PubSub Topic]] instance for each pub/sub topic,
then forwarding messages between these and local engine insntances.
It also maintains a database of known `NodeAdvert` and `TopicAdvert` messages.
--8<-- [end:purpose]

## Engine Components

- [[Router Messages]]
- [[Router Environment]]
- [[Router Dynamics]]

## Useful links

## Types

### `RouterEngine`

<!-- --8<-- [start:RouterEngine] -->
```juvix
RouterEngine : Type :=
  Engine
    RouterLocalState
    RouterMailboxState
    RouterTimerHandle
    RouterMatchableArgument
    RouterActionLabel
    RouterPrecomputation;
```
<!-- --8<-- [end:RouterEngine] -->

#### Example of a Router engine

<!-- --8<-- [start:RouterEngine] -->
```juvix
exampleRouterEngine : RouterEngine := mkEngine@{
  name := "router";
  behaviour := routerBehaviour;
  initEnv := routerEnvironmentExample;
};
```
<!-- --8<-- [end:RouterEngine] -->

where `routerEnvironmentExample` is defined as follows:

--8 TODO <-- "./router_environment.juvix.md:environment-example"

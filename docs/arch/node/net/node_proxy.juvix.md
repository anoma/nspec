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
    module arch.node.net.node_proxy;

    import prelude open;
    import arch.node.net.node_proxy_messages open;
    -- import arch.node.net.node_proxy_environment open;
    -- import arch.node.net.node_proxy_behaviour open;
    import arch.node.types.engine open;
    open template_environment_example;
    ```

# Node Proxy Engine

## Purpose

--8<-- [start:purpose]
The *Node Proxy* engine is responsible for
communication with one specific remote node.

It performs transport selection,
connection establishment and maintenance.

It forwards messages between local engine instances
and [[Transport Connection]] engine instances.

Connections may be ephemeral or permanent.
Ephemeral connections are established when the first message is sent to the node,
or when the remote node initiates a connection,
and not re-established automatically when the connection is lost.
Permanent connections are established when the *Node Proxy* is started,
and automatically re-established when the connection is lost.

The engine instance name corresponds to the remote `NodeID`.
--8<-- [end:purpose]

## Engine Components

- [[Node Proxy Messages]]
- [[Node Proxy Environment]]
- [[Node Proxy Dynamics]]

## Useful links

## Types

### `NodeProxyEngine`

<!-- --8<-- [start:NodeProxyEngine] -->
```juvix
NodeProxyEngine : Type :=
  Engine
    NodeProxyLocalState
    NodeProxyMailboxState
    NodeProxyTimerHandle
    NodeProxyMatchableArgument
    NodeProxyActionLabel
    NodeProxyPrecomputation;
```
<!-- --8<-- [end:NodeProxyEngine] -->

#### Example of a Node Proxy engine

<!-- --8<-- [start:NodeProxyEngine] -->
```juvix
exampleNodeProxyEngine : NodeProxyEngine := mkEngine@{
  name := "<node_id>";
  behaviour := nodeproxyBehaviour;
  initEnv := nodeproxyEnvironmentExample;
};
```
<!-- --8<-- [end:NodeProxyEngine] -->

where `nodeproxyEnvironmentExample` is defined as follows:

--8 TODO <-- "./node_proxy_environment.juvix.md:environment-example"

---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- node-proxy-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.node_proxy;

    import arch.node.net.node_proxy_messages open;
    import arch.node.net.node_proxy_config open;
    import arch.node.net.node_proxy_environment open;
    import arch.node.net.node_proxy_behaviour open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open node_proxy_config_example;
    open node_proxy_environment_example;
    open node_proxy_behaviour_example;
    ```

# Node Proxy Engine

## Purpose

<!-- --8<-- [start:purpose] -->
A *Node Proxy* engine is responsible for
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
<!-- --8<-- [end:purpose] -->

## Engine Components

- [[Node Proxy Messages]]
- [[Node Proxy Configuration]]
- [[Node Proxy Environment]]
- [[Node Proxy Behaviour]]

## Type

<!-- --8<-- [start:NodeProxyEngine] -->
```juvix
NodeProxyEngine : Type :=
  Engine
    NodeProxyLocalCfg
    NodeProxyLocalState
    NodeProxyMailboxState
    NodeProxyTimerHandle
    NodeProxyActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:NodeProxyEngine] -->

### Instantiation

<!-- --8<-- [start:exNodeProxyEngine] -->
```juvix
exNodeProxyEngine : NodeProxyEngine :=
  mkEngine@{
    cfg := exNodeProxyCfg;
    env := exNodeProxyEnv;
    behaviour := exNodeProxyBehaviour;
  };
```
<!-- --8<-- [end:exNodeProxyEngine] -->

Where `exNodeProxyCfg` is defined as follows:

--8<-- "./docs/arch/node/net/node_proxy_config.juvix.md:exNodeProxyCfg"

`exNodeProxyEnv` is defined as follows:

--8<-- "./docs/arch/node/net/node_proxy_environment.juvix.md:exNodeProxyEnv"

and `exNodeProxyBehaviour` is defined as follows:

--8<-- "./docs/arch/node/net/node_proxy_behaviour.juvix.md:exNodeProxyBehaviour"

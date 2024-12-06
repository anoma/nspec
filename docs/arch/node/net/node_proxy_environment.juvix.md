---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- node-proxy-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.node_proxy_environment;

    import arch.node.net.node_proxy_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Node Proxy Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox states

```juvix
syntax alias NodeProxyMailboxState := Unit;
```

## Local state

```juvix
type NodeProxyLocalState := mkNodeProxyLocalState;
```

## Timer Handle

```juvix
NodeProxyTimerHandle : Type := Unit;
```

## Timestamped Trigger

<!-- --8<-- [start:TemplateTimestampedTrigger] -->
```juvix
NodeProxyTimestampedTrigger : Type :=
  TimestampedTrigger
    NodeProxyTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateTimestampedTrigger] -->

## The Node Proxy Environment

### `NodeProxyEnv`

<!-- --8<-- [start:NodeProxyEnv] -->
```juvix
NodeProxyEnv : Type :=
  EngineEnv
    NodeProxyLocalState
    NodeProxyMailboxState
    NodeProxyTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:NodeProxyEnv] -->

#### Instantiation

<!-- --8<-- [start:nodeProxyEnv] -->
```juvix extract-module-statements
module node_proxy_environment_example;

nodeProxyEnv : NodeProxyEnv :=
  mkEngineEnv@{
    localState := mkNodeProxyLocalState;
    mailboxCluster := Map.empty;
    acquaintances := Set.empty;
    timers := []
  };

end;
```
<!-- --8<-- [end:nodeProxyEnv] -->

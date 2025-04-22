---
icon: octicons/container-24
search:
  exclude: false
tags:
  - tutorial
  - example
---

??? code "Juvix imports"

    ```juvix
    module tutorial.engines.template_minimum_environment;

    import tutorial.engines.template_minimum_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Template Minimum Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

### `TemplateMinimumMailboxState`

<!-- --8<-- [start:TemplateMinimumMailboxState] -->
```juvix
TemplateMinimumMailboxState : Type := Unit;
```
<!-- --8<-- [end:TemplateMinimumMailboxState] -->

## Local state

### `TemplateMinimumLocalState`

<!-- --8<-- [start:TemplateMinimumLocalState] -->
```juvix
type TemplateMinimumLocalState :=
  mk;
```
<!-- --8<-- [end:TemplateMinimumLocalState] -->

## Timer handles

### `TemplateMinimumTimerHandle`

<!-- --8<-- [start:TemplateMinimumTimerHandle] -->
```juvix
TemplateMinimumTimerHandle : Type := Unit;
```
<!-- --8<-- [end:TemplateMinimumTimerHandle] -->

### `TemplateMinimumTimestampedTrigger`

<!-- --8<-- [start:TemplateMinimumTimestampedTrigger] -->
```juvix
TemplateMinimumTimestampedTrigger : Type :=
  TimestampedTrigger
    TemplateMinimumTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateMinimumTimestampedTrigger] -->

## Engine Environment

### `TemplateMinimumEnv`

<!-- --8<-- [start:TemplateMinimumEnv] -->
```juvix
TemplateMinimumEnv : Type :=
  EngineEnv
    TemplateMinimumLocalState
    TemplateMinimumMailboxState
    TemplateMinimumTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateMinimumEnv] -->

#### Instantiation

<!-- --8<-- [start:exTemplateMinimumEnv] -->
```juvix extract-module-statements
module template_minimum_environment_example;

  exTemplateMinimumEnv : TemplateMinimumEnv :=
    EngineEnv.mk@{
      localState := TemplateMinimumLocalState.mk;
      mailboxCluster := Map.empty;
      acquaintances := Set.Set.empty;
      timers := []
    };
end;
```
<!-- --8<-- [end:exTemplateMinimumEnv] -->

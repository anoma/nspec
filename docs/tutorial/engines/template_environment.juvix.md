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
    module tutorial.engines.template_environment;

    import tutorial.engines.template_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Template Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

??? code "Auxiliary Juvix code"

    ```juvix
    syntax alias MailboxOneOne := Nat;
    syntax alias MailboxTwoOne := String;
    syntax alias MailboxTwoTwo := Bool;
    ```

### `TemplateMailboxStateFirstKind FirstKindMailboxState`

<!-- --8<-- [start:FirstKindMailboxState] -->
```juvix
type FirstKindMailboxState := mkFirstKindMailboxState@{
  fieldOne : MailboxOneOne
};
```
<!-- --8<-- [end:FirstKindMailboxState] -->

This is one family of mailbox states without much complexity.

???+ code "Arguments"

    `fieldOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.


### `TemplateMailboxStateSecondKind SecondKindMailboxState`

<!-- --8<-- [start:SecondKindMailboxState] -->
```juvix
type SecondKindMailboxState := mkSecondKindMailboxState@{
  fieldOne : MailboxTwoOne;
  fieldTwo : MailboxTwoTwo
};
```
<!-- --8<-- [end:SecondKindMailboxState] -->

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

???+ code "Arguments"

    `fieldOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `fieldTwo`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateMailboxState`

<!-- --8<-- [start:TemplateMailboxState] -->
```juvix
type TemplateMailboxState :=
  | TemplateMailboxStateFirstKind FirstKindMailboxState
  | TemplateMailboxStateSecondKind SecondKindMailboxState;
```
<!-- --8<-- [end:TemplateMailboxState] -->

## Local state

??? code "Auxiliary Juvix code"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    <!-- --8<-- [start:CustomData] -->
    ```juvix
    type CustomData := mkCustomData { word : String };
    ```
    <!-- --8<-- [end:CustomData] -->

    ???+ code "Arguments"

        `word`

        : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateLocalState`

<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState :=
  mkTemplateLocalState@{
    taskQueue : CustomData
  };
```
<!-- --8<-- [end:TemplateLocalState] -->

???+ code "Arguments"

    `taskQueue`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Timer handles

??? code "Auxiliary Juvix code"

    <!-- --8<-- [start:ArgOne] -->
    ```juvix
    syntax alias ArgOne := Nat;
    ```
    <!-- --8<-- [end:ArgOne] -->

### `TemplateTimerHandleFirstOption FirstOptionTimerHandle`

<!-- --8<-- [start:FirstOptionTimerHandle] -->
```juvix
type FirstOptionTimerHandle := mkFirstOptionTimerHandle@{
  argOne : ArgOne
};
```
<!-- --8<-- [end:FirstOptionTimerHandle] -->

Lorem ipsum dolor sit amet, consectetur adipiscing elit. The following code is
an example of this case.

???+ code "Arguments"

    `argOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateTimerHandleSecondOption SecondOptionTimerHandle`

<!-- --8<-- [start:SecondOptionTimerHandle] -->
```juvix
type SecondOptionTimerHandle := mkSecondOptionTimerHandle@{
  argOne : String;
  argTwo : Bool
};
```
<!-- --8<-- [end:SecondOptionTimerHandle] -->

???+ code "Arguments"

    `argOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `argTwo`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateTimerHandle`

<!-- --8<-- [start:TemplateTimerHandle] -->
```juvix
type TemplateTimerHandle :=
  | TemplateTimerHandleFirstOption FirstOptionTimerHandle
  | TemplateTimerHandleSecondOption SecondOptionTimerHandle;
```
<!-- --8<-- [end:TemplateTimerHandle] -->

### `TemplateTimestampedTrigger`

<!-- --8<-- [start:TemplateTimestampedTrigger] -->
```juvix
TemplateTimestampedTrigger : Type :=
  TimestampedTrigger
    TemplateTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateTimestampedTrigger] -->

## Engine Environment

### `TemplateEnv`

<!-- --8<-- [start:TemplateEnv] -->
```juvix
TemplateEnv : Type :=
  EngineEnv
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateEnv] -->

#### Instantiation

<!-- --8<-- [start:exTemplateEnv] -->
```juvix extract-module-statements
module template_environment_example;

  exTemplateEnv : TemplateEnv :=
    mkEngineEnv@{
      localState := mkTemplateLocalState@{
        taskQueue := mkCustomData@{
          word := "taskQueue"
        }
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    };
end;
```
<!-- --8<-- [end:exTemplateEnv] -->

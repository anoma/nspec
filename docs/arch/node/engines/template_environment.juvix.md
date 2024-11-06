---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.template_environment;
    import prelude open;
    import arch.node.types.engine open;
    import arch.node.engines.template_messages open;
    ```

# Template Environment

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Mailbox state types

??? quote "Auxiliary Juvix code"

    ```juvix
    syntax alias MailboxOneOne := Nat;
    syntax alias MailboxTwoOne := String;
    syntax alias MailboxTwoTwo := Bool;
    ```

### TemplateMailboxState constructors

??? quote "TemplateMailboxStateFirstKind FirstKindMailboxState"

    <!-- --8<-- [start:FirstKindMailboxState] -->
    ```juvix
    type FirstKindMailboxState := mkFirstKindMailboxState {
      fieldOne : MailboxOneOne
    };
    ```
    <!-- --8<-- [end:FirstKindMailboxState] -->


    This is one family of mailbox states without much complexity.

    `fieldOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.


??? quote "TemplateMailboxStateSecondKind SecondKindMailboxState"

    <!-- --8<-- [start:SecondKindMailboxState] -->
    ```juvix
    type SecondKindMailboxState := mkSecondKindMailboxState {
      fieldOne : MailboxTwoOne;
      fieldTwo : MailboxTwoTwo
    };
    ```
    <!-- --8<-- [end:SecondKindMailboxState] -->

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `fieldOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `fieldTwo`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### TemplateMailboxState

<!-- --8<-- [start:TemplateMailboxState] -->
```juvix
type TemplateMailboxState :=
  | TemplateMailboxStateFirstKind FirstKindMailboxState
  | TemplateMailboxStateSecondKind SecondKindMailboxState;
```
<!-- --8<-- [end:TemplateMailboxState] -->

## Local state

??? quote "Auxiliary Juvix code"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    <!-- --8<-- [start:CustomData] -->
    ```juvix
    type CustomData := mkCustomData { word : String };
    ```
    <!-- --8<-- [end:CustomData] -->

    `word`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### TemplateLocalState
<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState :=
  mkTemplateLocalState {
    taskQueue : CustomData
};
```
<!-- --8<-- [end:TemplateLocalState] -->

## Timer handles

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:ArgOne] -->
    ```juvix
    syntax alias ArgOne := Nat;
    ```
    <!-- --8<-- [end:ArgOne] -->

### TemplateTimerHandle constructors

??? quote "FirstOptionTimerHandle"

    <!-- --8<-- [start:FirstOptionTimerHandle] -->
    ```juvix
    type FirstOptionTimerHandle := mkFirstOptionTimerHandle {
      argOne : ArgOne
    };
    ```
    <!-- --8<-- [end:FirstOptionTimerHandle] -->

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. The following code is
    an example of this case.

    `argOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

??? quote "SecondOptionTimerHandle"

    <!-- --8<-- [start:SecondOptionTimerHandle] -->
    ```juvix
    type SecondOptionTimerHandle := mkSecondOptionTimerHandle {
    argOne : String;
    argTwo : Bool
    };
    ```
    <!-- --8<-- [end:SecondOptionTimerHandle] -->

    `argOne`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `argTwo`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### TemplateTimerHandle

<!-- --8<-- [start:TemplateTimerHandle] -->
```juvix
type TemplateTimerHandle :=
  | TemplateTimerHandleFirstOption FirstOptionTimerHandle
  | TemplateTimerHandleSecondOption SecondOptionTimerHandle;
```
<!-- --8<-- [end:TemplateTimerHandle] -->

## The Template Environment

### TemplateEnvironment

<!-- --8<-- [start:TemplateEnvironment] -->
```juvix
TemplateEnvironment : Type :=
  EngineEnvironment
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle;
```
<!-- --8<-- [end:TemplateEnvironment] -->

#### Instantiation

<!-- --8<-- [start:templateEnvironment] -->
```juvix extract-module-statements
module template_environment_example;

  templateEnvironment : TemplateEnvironment :=
    mkEngineEnvironment@ {
      name := "template";
      localState := mkTemplateLocalState@{
        taskQueue := mkCustomData@{
          word := "taskQueue"
        }
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:templateEnvironment] -->

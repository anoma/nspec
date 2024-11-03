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

# Template Environment

??? quote "Juvix preamble"

    ```juvix
    module arch.node.engines.template_environment;
    import prelude open;
    import arch.node.types.engine open;
    import arch.node.engines.template_messages open;
    ```

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Mailbox states

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:MailboxOneOne] -->
    ```juvix
    syntax alias MailboxOneOne := Nat;
    ```
    <!-- --8<-- [end:MailboxOneOne] -->

    <!-- --8<-- [start:MailboxTwoOne] -->
    ```juvix
    syntax alias MailboxTwoOne := String;
    ```
    <!-- --8<-- [end:MailboxTwoOne] -->

    <!-- --8<-- [start:MailboxTwoTwo] -->
    ```juvix
    syntax alias MailboxTwoTwo := Bool;
    ```
    <!-- --8<-- [end:MailboxTwoTwo] -->

### FirstKindMailboxState

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

### SecondKindMailboxState

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

    <!-- --8<-- [start:NiceState] -->
    ```juvix
    type NiceState := mkNiceState { word : String };
    ```
    <!-- --8<-- [end:NiceState] -->

    `word`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState :=
  mkTemplateLocalState {
    taskQueue : NiceState
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
### FirstOptionTimerHandle

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

### SecondOptionTimerHandle

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

## TemplateEnvironment type

<!-- --8<-- [start:TemplateEnvironment] -->
```juvix
TemplateEnvironment : Type :=
  EngineEnvironment
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle;
```
<!-- --8<-- [end:TemplateEnvironment] -->

## An example of a TemplateEnvironment

<!-- --8<-- [start:templateEnvironmentExample] -->
```juvix extract-module-statements
module template_environment_example;

  templateEnvironmentExample : TemplateEnvironment :=
    mkEngineEnvironment@ {
      name := "template";
      localState := mkTemplateLocalState@{
        taskQueue := mkNiceState@{
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
<!-- --8<-- [end:templateEnvironmentExample] -->

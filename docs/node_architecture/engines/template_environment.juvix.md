---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- mytag1
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.template_environment;
    import prelude open;
    import node_architecture.types.engine_family open;
    import node_architecture.engines.template_overview open;
    ```

# `Template` Environment

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Mailbox states

<!-- --8<-- [start:mailbox_auxiliary] -->
??? note "Auxiliary Juvix code"

    ```juvix
    syntax alias MailboxOneOne := Nat;
    syntax alias MailboxTwoOne := String;
    syntax alias MailboxTwoTwo := Bool;
    ```
<!-- --8<-- [end:mailbox_auxiliary] -->

<!-- --8<-- [start:TemplateMailboxState] -->
```juvix
type TemplateMailboxState :=
| TemplateMailboxStateOne { fieldOne : MailboxOneOne }
| TemplateMailboxStateTwo { fieldOne : MailboxTwoOne; fieldTwo : MailboxTwoTwo }
;
```
<!-- --8<-- [end:TemplateMailboxState] -->

### `Template`

This is one family of mailbox states without much complexity.

??? example

    <!-- --8<-- [start:state_one_example] -->
    ```juvix extract-module-statements 1
    module state_one_example;
      TemplateMailboxStateOneExample : TemplateMailboxState := TemplateMailboxStateOne@{
        fieldOne := 1
      };
    end;
    ```
    <!-- --8<-- [end:state_one_example] -->

`fieldOne`

: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `stateTwo`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Local state

??? note "Auxiliary Juvix code"

    We use [Fibonacci heaps](https://en.wikipedia.org/wiki/Fibonacci_heap) to
    keep track of tasks to be performed. Note that we use
    [Borsh](https://borsh.io/) for deserialisation of Fibonacci heaps.

    ```juvix
    type FakeFibonacciHeap := mkFakeFibonacciHeap {
        stringRepresentation : String
    };
    ```

<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState := mkTemplateLocalState {
      taskQueue : FakeFibonacciHeap
};
```
<!-- --8<-- [end:TemplateLocalState] -->

`stringRepresentation`

: This is a representation of the Fibonacci heap, using
[Borsh](https://borsh.io/).

## Timer handles

??? note "Auxiliary Juvix code"

    ```juvix
    syntax alias ArgOne := Nat;
    ```

<!-- --8<-- [start:TemplateTimerHandle] -->
```juvix
type TemplateTimerHandle :=
  | -- --8<-- [start:handleOne]
    timerHandleOne { argOne : ArgOne }
    -- --8<-- [end:handleOne]
  | timerHandleTwo { argOne : String; argTwo : Bool }
  ;
```
<!-- --8<-- [end:TemplateTimerHandle] -->

### `timerHandleOne`

The first kind of timer handle.

`argOne`

: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `timerHandleTwo`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `timerHandleTwo`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Example of a time handle

```juvix extract-module-statements 1
module handle_one_example;

handleOneExample : TemplateTimerHandle := timerHandleOne@{
  argOne := 7;
};
end;
```

## Environment summary

We have finished all the type definitions,
there is nothing to explain in the template
as the code is self-explanatory.

```juvix
TemplateEnvironment : Type :=
  EngineEnvironment
  TemplateLocalState
  TemplateMsg
  TemplateMailboxState
  TemplateTimerHandle;
```


## Example of an environment

```juvix extract-module-statements 1
module template_environment_example;

  templateEnvironmentExample : TemplateEnvironment :=
    mkEngineEnvironment@ {
      name := Left "template"; -- Name
      localState := mkTemplateLocalState@{
        taskQueue := mkFakeFibonacciHeap@{
          stringRepresentation := "taskQueue"
        }
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;

end;
```


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
| -- --8<-- [start:TemplateMailboxStateOne]
  TemplateMailboxStateOne { fieldOne : MailboxOneOne }
  -- --8<-- [end:TemplateMailboxStateOne]
| -- --8<-- [start:TemplateMailboxStateTwo]
  TemplateMailboxStateTwo { fieldOne : MailboxTwoOne; fieldTwo : MailboxTwoTwo }
  -- --8<-- [end:TemplateMailboxStateTwo]
;
```
<!-- --8<-- [end:TemplateMailboxState] -->

### `TemplateMailboxStateOne`

This is one family of mailbox states without much complexity.

`fieldOne`

: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateMailboxStateTwo`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

`fieldOne`

: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

`fieldTwo`

: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

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

    `stringRepresentation`

    : This is a representation of the Fibonacci heap, using
    [Borsh](https://borsh.io/).


<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState := mkTemplateLocalState {
      taskQueue : FakeFibonacciHeap
};
```
<!-- --8<-- [end:TemplateLocalState] -->


## Timer handles

??? note "Auxiliary Juvix code"

    ```juvix
    syntax alias ArgOne := Nat;
    ```

<!-- --8<-- [start:TemplateTimerHandle] -->
```juvix
type TemplateTimerHandle :=
  | -- --8<-- [start:TemplateTimerHandleOne]
    TemplateTimerHandleOne { argOne : ArgOne }
    -- --8<-- [end:TemplateTimerHandleOne]
  | -- --8<-- [start:TemplateTimerHandleTwo] 
    TemplateTimerHandleTwo { argOne : String; argTwo : Bool }
    -- --8<-- [end:TemplateTimerHandleTwo]
  ;
```
<!-- --8<-- [end:TemplateTimerHandle] -->

### `TemplateTimerHandleOne`

Lorem ipsum dolor sit amet, consectetur adipiscing elit. The following code is
an example of this case.

```juvix extract-module-statements 1
module handle_one_example;

  handleOneExample : TemplateTimerHandle := TemplateTimerHandleOne@{
    argOne := 7;
  };
end;
```

`argOne`

: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateTimerHandleTwo`

Lorem ipsum dolor sit amet, consectetur adipiscing elit. The following code is
an example of this case.

```juvix extract-module-statements 1
module handle_two_example;

  handleTwoExample : TemplateTimerHandle := TemplateTimerHandleTwo@{
    argOne := "hello"; argTwo := true;
  };
end;
```

## Environment summary

We have finished all the type definitions, there is nothing to explain in the
template as the code is self-explanatory.

```juvix
TemplateEnvironment : Type :=
  EngineEnvironment
  TemplateLocalState
  TemplateMsg
  TemplateMailboxState
  TemplateTimerHandle;
```


## Example of a `Template` environment

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


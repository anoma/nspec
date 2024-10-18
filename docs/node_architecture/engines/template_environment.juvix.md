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
    import node_architecture.engines.template_messages open;
    ```

# `Template` Environment

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Mailbox states

<!-- --8<-- [start:mailbox_auxiliary] -->
??? quote "Auxiliary Juvix code"

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

??? quote "Auxiliary Juvix code"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    ```juvix
    type NiceState := mkNiceState { word : String };
    ```

    `stringRepresentation`

    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.


<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState := mkTemplateLocalState {
      taskQueue : NiceState
};
```
<!-- --8<-- [end:TemplateLocalState] -->


## Timer handles

??? quote "Auxiliary Juvix code"

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

```juvix extract-module-statements
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

```juvix extract-module-statements
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
  TemplateMailboxState
  TemplateTimerHandle;
```


## Example of a `Template` environment

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

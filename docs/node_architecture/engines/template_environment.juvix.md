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

<!-- --8<-- [start:juvix-preamble] -->
??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.template_environment;
    import prelude open;
    import node_architecture.types.engine_family open;
    ```

<!-- --8<-- [end:juvix-preamble] -->

# Template Environment

[...]

## Overview

[...]

## Messages

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:message_auxiliary] -->
    ```juvix
    syntax alias MethodOneArgOne := Nat;
    syntax alias MethodOneArgTwo := Nat;
    syntax alias MethodOneArgThree := Nat;
    syntax alias MethodTwoArgOne := Nat;
    syntax alias MethodFourArgOne := Unit;
    syntax alias MethodFourArgTwo := Unit;
    ```
    <!-- --8<-- [end:message_auxiliary] -->


<!-- --8<-- [start:TemplateMessageType] -->
```juvix
type TemplateMessage :=
  | -- --8<-- [start:messageOne]
    messageOne {
      argOneOne : MethodOneArgOne;
      argTwo : MethodOneArgTwo;
      argThree : MethodOneArgThree
  }
    -- --8<-- [end:messageOne]
  | messageTwo {
      argOne : MethodTwoArgOne
  }
  | messageThree {}
  | messageFour {
      argOne : MethodFourArgOne;
      argTwo : MethodFourArgTwo
    }
  ;
```
<!-- --8<-- [end:TemplateMessageType] -->

### messageOne

If an [engine family name] receives a messageOne-message,
it will store argTwo, if argOne and argThree satisfy some properties.

<!-- --8<-- [start:message_one_example] -->
```juvix
module message_one_example;
  example_message_one : TemplateMessage := messageOne@{
    argOneOne := 1;
    argTwo := 2;
    argThree := 3
    };
end;
```
<!-- --8<-- [end:message_one_example] -->

argOne

: The `argOne` is almost self-explanatory, but we need to talk about it.

argTwo

: This is the second argument.

argThree

: This is the last argument and here we actually
  can describe more detail about the property about `argOne`
  and `argThree` mentioned above

### messageTwo

[...]

### messageThree

[...]

### messageFour

[...]

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
| -- --8<-- [start:stateOne]
  stateOne { fieldOne : MailboxOneOne }
  -- --8<-- [end:stateOne]
| -- --8<-- [start:stateTwo]
  stateTwo { fieldOne : MailboxTwoOne; fieldTwo : MailboxTwoTwo }
  -- --8<-- [end:stateTwo]
;
```
<!-- --8<-- [end:TemplateMailboxState] -->

### stateOne

This is one family of mailbox states without much complexity.

<!-- --8<-- [start:state_one_example] -->
```juvix
module state_one_example;
stateOneExample : TemplateMailboxState := stateOne@{
  fieldOne := 1
};
end;
```
<!-- --8<-- [end:state_one_example] -->

fieldOne

: A Nat is a Nat is a Nat.

### stateTwo

[...]

## Local state

We use [Fibonacci heaps](https://en.wikipedia.org/wiki/Fibonacci_heap)
to keep track of tasks to be performed.
Note that we use [Borsh](https://borsh.io/)
for deserialisation of Fibonacci heaps.

<!-- --8<-- [start:local_state_auxiliary] -->
??? note "Auxiliary Juvix code"

    ```juvix
    someComplicatedFunction : Type -> Type := undef;
    SomeAuxiliaryDataType : Type := undef;
    ```
<!-- --8<-- [end:local_state_auxiliary] -->


<!-- --8<-- [start:FakeFibonacciHeap] -->
```juvix
type FakeFibonacciHeap := mkFakeFibonacciHeap {
    stringRepresentation : String
};
```
<!-- --8<-- [end:FakeFibonacciHeap] -->

<!-- --8<-- [start:TemplateLocalState] -->
```juvix
type TemplateLocalState := mkTemplateLocalState {
      taskQueue : FakeFibonacciHeap
};
```
<!-- --8<-- [end:TemplateLocalState] -->

stringRepresentation

: This is a representation of the Fibonacci heap,
using [Borsh](https://borsh.io/).

## Timer handles

<!-- --8<-- [start:timer_auxiliary] -->
??? note "Auxiliary Juvix code"

    ```juvix
    syntax alias ArgOne := Nat;
    ```
<!-- --8<-- [end:timer_auxiliary] -->

<!-- --8<-- [start:TemplateTimerHandle] -->
```juvix
type TemplateTimerHandle :=
| -- --8<-- [start:handleOne]
  timerHandleOne { argOne : ArgOne }
  -- --8<-- [end:handleOne]
| timerHandleTwo { argOne : String; argTwo : Bool }
| timerHandleThree {
};
```
<!-- --8<-- [end:TemplateTimerHandle] -->

### timerHandleOne

The first kind of timer handle.

<!-- --8<-- [start:handle_one_example] -->
```juvix
module handle_one_example;

handleOneExample : TemplateTimerHandle := timerHandleOne@{
  argOne := 7;
};
end;
```
<!-- --8<-- [end:handle_one_example] -->

argOne

: This is argument №1.

### timerHandleTwo

[...]

### timerHandleTwo

[...]

## Environment summary

We have finished all the type definitions,
there is nothing to explain in the template
as the code is self-explanatory.

<!-- --8<-- [start:TemplateEnvironment] -->
```juvix
TemplateEnvironment : Type :=
  EngineEnvironment
  TemplateLocalState
  TemplateMessage
  TemplateMailboxState
  TemplateTimerHandle;
```
<!-- --8<-- [end:TemplateEnvironment] -->


??? todo "fix example 👇"

    ```juvix
    module template_environment_example;
    templateEnvironmentExample : TemplateEnvironment :=
      mkEngineEnvironment@ {
        name := undef; -- Name
        localState := undef; -- S
        mailboxCluster := undef; -- Map MailboxID (Mailbox I M);
        acquaintances := undef; -- Set Name
        timers := [] -- List (Timer H)
      }
    ;
    end;
    ```


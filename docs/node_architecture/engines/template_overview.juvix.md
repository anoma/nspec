--- <!-- (1)! -->
icon: octicons/gear-16  <!-- (2)! -->
search:
  exclude: false
categories:
- engine-family <!-- (3)! -->
tags:
- mytag1 <!-- (4)! -->
- engine-overview
---


??? info "Juvix preamble"

    ```juvix
    module node_architecture.engines.template_overview;
    import prelude open;
    ```

# Engine Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut purus eget sapien. Nulla facilisi.

# `Template` Engine Family  

## Purpose  

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut purus eget sapien. Nulla facilisi.

## Message interface

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


<!-- --8<-- [start:TemplateMessage] -->
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
  ;
```
<!-- --8<-- [end:TemplateMessage] -->

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


## Message sequence diagrams  

### [Title of message sequence diagram ⟨𝑖⟩]  

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut purus eget sapien. Nulla facilisi.

## Engine Components  

??? note [[Template Engine Environment|Engine environment]]  

     
   --8< "./docs/node_architecture/engines/template_environment.juvix.md"

??? note [[Template Engine Dynamics|Engine dynamics]]  

   --8< "./docs/node_architecture/engines/template_dynamics.juvix.md"

## Useful links

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut purus eget sapien. Nulla facilisi.
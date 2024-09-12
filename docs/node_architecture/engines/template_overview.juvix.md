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

    ```juvix
    type TemplateMsg := DefineYourConstructorHere;
    ```

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
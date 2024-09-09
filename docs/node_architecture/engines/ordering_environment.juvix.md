---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- ordering
- engine-environment
---


??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.ordering_environment;
    import prelude open;
    import node_architecture.types.engine_family open;
    ```


!!! warning "[Under construction]"

    This (Juvix) page is still under construction, needs to be
    updated with the latest changes in the engine family type.

# Template Environment

## Overview

[...]

## Messages

[...]

??? note "Auxiliary Juvix code

    [...]

```juvix
type XMessage :=
  | -- <!-- --8<-- [start:message1] -->
  [Message constructor 1]
  -- <!---8<-- - [end:message1] -->
  | [Message constructor ...]
```a

### [Message constructor 1]

If an [engine family] engine receives a message of
this type, it will [...]

<!-- Code snippet -->

<!-- Message tag documentation and example -->

### [Message constructor ...]

[...]

## Mailbox states

??? note "Auxiliary Juvix code

    [...]

[...]

## Local state

[...]

## Timer handles

??? note "Auxiliary Juvix code"

    [...]

[...]

## Environment summary

[...]
---
icon: octicons/gear-16
search:
  exclude: false
tags:
- engines
- conventions
---

??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.template;

    import node_architecture.engines.template_messages open public;
    import node_architecture.engines.template_environment open public;
    import node_architecture.engines.template_behaviour open public;

    import prelude open;
    import node_architecture.types.identities open;
    import node_architecture.types.engine open;
    ```

# Template Engine

## Purpose

Brief summary of the purpose of the engine.

## Components

- [[Template Messages]]
- [[Template Environment]]
- [[Template Behaviour]]

## Useful links

- Some
- Useful
- Links

## Types

### `TemplateBehaviour`

<!-- --8<-- [start:TemplateBehaviour] -->
```juvix
TemplateBehaviour :
  EngineBehaviour
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateMatchableArgument
    TemplateActionLabel
    TemplatePrecomputation
  := mkEngineBehaviour@{
    guards := [messageOneGuard];
    action := templateAction;
    conflictSolver := templateConflictSolver;
  }
  ;
```
<!-- --8<-- [end:TemplateBehaviour] -->

### `TemplateEngine`

<!-- --8<-- [start:TemplateEngine] -->
TODO
<!-- --8<-- [end:TemplateEngine] -->

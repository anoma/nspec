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
    module arch.node.engines.template;
      import prelude open;
      import arch.node.engines.template_messages open public;
      import arch.node.engines.template_environment open public;
      import arch.node.engines.template_behaviour open public;
      import arch.node.types.engine open;
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

---
icon: octicons/project-template-24
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
      import arch.node.engines.template_overview open public;
      import arch.node.engines.template_environment open public;
      import arch.node.engines.template_dynamics open public;
      import arch.node.types.engine_family as Anoma;
    ```

# `Template` engine family type

<!-- --8<-- [start:template-engine-family] -->
```juvix
TemplateEngineFamily :
  Anoma.EngineFamily
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateMatchableArgument
    TemplateActionLabel
    TemplatePrecomputation
  := Anoma.mkEngineFamily@{
    guards := [messageOneGuard];
    action := templateAction;
    conflictSolver := templateConflictSolver;
  }
  ;
```
<!-- --8<-- [end:ticker-engine-family] -->



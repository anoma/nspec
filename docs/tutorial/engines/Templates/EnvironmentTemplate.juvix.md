---
icon: octicons/check-24
search:
  exclude: false
---

# Engine Family Environment

??? note "Juvix module" 

    ```juvix
    module tutorial.Templates.EnvironmentTemplate;
    import architecture-2.Prelude open;
    import architecture-2.types.EngineFamily as EngineFamily;
    open EngineFamily using {
        Engine;
        EngineEnvironment;
        EngineFamily;
        mkActionResult;
        mkEngine;
        mkEngineEnvironment;
        mkEngineFamily;
        mkGuardedAction
    };
    open EngineFamily.EngineEnvironment;
    import tutorial.engines.Ticker.Env open public;
    import tutorial.engines.Ticker.Actions open public;
    ```

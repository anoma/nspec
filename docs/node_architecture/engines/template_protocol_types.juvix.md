---
icon: octicons/project-template-24
search:
  exclude: false
  boost: 2
tags:
  - juvix
  - engines
  - template
  - protocol
---


The following is the module for the protocol level types of the template.

??? info "Juvix imports"

    ```juvix
    module tutorial.engines.template.template_protocol_types;
    import prelude open;
    ```

??? "Juvix auxiliary code"

    <!-- --8<-- [start:auxiliary-juvix-code] -->
    ```juvix
    syntax alias EngineOneMessage := Unit;
    syntax alias EngineTwoMessage := Unit;
    syntax alias EngineThreeMessage := Unit;
    syntax alias EngineFourMessage := Unit;

    syntax alias EngineOneEnvironment := Unit;
    syntax alias EngineTwoEnvironment := Unit;
    syntax alias EngineThreeEnvironment := Unit;
    syntax alias EngineFourEnvironment := Unit;
    ```
    <!-- --8<-- [end:auxiliary-juvix-code] -->

The type for protocol level messages.

<!-- --8<-- [start:ProtocolMessage] -->
```juvix
type ProtocolMessage :=
  | EngineOneMsg EngineOneMessage
  | EngineTwoMsg EngineTwoMessage
  | EngineThreeMsg EngineThreeMessage
  | EngineFourMsg EngineFourMessage;
```
<!-- --8<-- [end:ProtocolMessage] -->

The type for protocol level engine environments.
<!-- --8<-- [start:ProtocolEnvironment] -->
```juvix
type ProtocolEnvironment :=
  | EngineOneEnv EngineOneEnvironment
  | EngineTwoEnv EngineTwoEnvironment
  | EngineThreeEnv EngineThreeEnvironment
  | EngineFourEnv EngineFourEnvironment;
```
<!-- --8<-- [end:ProtocolEnvironment] -->

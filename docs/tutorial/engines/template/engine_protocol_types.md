---
icon: octicons/project-template-24
search:
  exclude: false
---


!!! note "Juvix protocol-level types"

    We also have to write (and later import)
    protocol-level type descriptions.
    These are two type declarations.

    Protocol-level message type

    : The name of the message type is the name of the protocol in which the engines take part,
    i.e., `Anoma` for the Anoma specification,
    followed by `ProtocolMessage`.
    This is an algebraic data type with one constructor per engine family
    that takes as argument a message of the respective engine family.

    : 👉 _This type is **the** type used for sending messages._

    Protocol-level environment type

    : Similarly, for engine environments, we have a type as above,
    but with `ProtocolEnvironment` instead of `ProtocolMessage`,
    and constructors taking environments from the respective engine families.

    : 👉 _This type is **the** type used for creating new engine instances._

    See the file `engine_protocol_type.juvix`.
    Note that for the purpose of these two types,
    the [[Engine Family Hierarchy]] is "flattened",
    i.e., the algebraic data type does not encode the hiearchy of engine families.

The following is the module for the protocol level types of the template.

```juvix
module tutorial.engines.template.template_protocol_types;
import prelude open;

syntax alias EngineOneMessage := Unit;
syntax alias EngineTwoMessage := Unit;
syntax alias EngineThreeMessage := Unit;
syntax alias EngineFourMessage := Unit;

syntax alias EngineOneEnvironment := Unit;
syntax alias EngineTwoEnvironment := Unit;
syntax alias EngineThreeEnvironment := Unit;
syntax alias EngineFourEnvironment := Unit;

--- the type for protocol level messages
type ProtocolMessage :=
  | EngineOneMsg EngineOneMessage
  | EngineTwoMsg EngineTwoMessage
  | EngineThreeMsg EngineThreeMessage
  | EngineFourMsg EngineFourMessage;

--- the type for protocol level engine environments
type ProtocolEnvironment :=
  | EngineOneEnv EngineOneEnvironment
  | EngineTwoEnv EngineTwoEnvironment
  | EngineThreeEnv EngineThreeEnvironment
  | EngineFourEnv EngineFourEnvironment;
```

---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engines
- conventions
---

<!-- Tobias, add here any specific, short, rule you may consider people
need to follow when writing engine families. I wrote a few examples below. -->

## Naming conventions

- **Engine Files and folders**: Named in lowercase using `snake_case` format.
- **File extension**: Files with overview, environment, and dynamics content
  must end with the `.juvix.md` extension. These files must be written in Juvix
  Markdown and include Juvix code snippets starting with a top-level module
  declaration. However, there is no need to include Juvix code if it's not
  necessary, but the module declaration is required.

- **Naming prefix**: The engine family's name is used as a prefix for these
  files. For example, the Ticker engine family would have the following files:

    - `ticker_overview.md`
    - `ticker_environment.juvix.md`
    - `ticker_dynamics.juvix.md`
    - `ticker_protocol_types.juvix.md`

### Directory Structure

The files are organized in the following tree view:

```plaintext
node_architecture/
└── ...
└── engines/
    ├── ...
    ├── myengine_overview.md
    ├── myengine_environment.juvix.md
    ├── myengine_dynamics.juvix.md
    └── myengine_protocol_types.juvix.md
...
└── myengine.juvix
```

In this structure, `myengine.juvix` is a Juvix module with the
following content that imports the three files mentioned above:

```juvix
module node_architecture.engines.myengine;
import node_architecture.engines.myengine_environment open public;
import node_architecture.engines.myengine_dynamics open public;
import node_architecture.engines.myengine_protocol_types open public;
```

!!! note

    To ensure new Juvix files are checked always, add this module to the
    `everything.juvix.md` file in the "Engines" section:

    ```diff
    module everything;

    {- Engines -}
    +import node_architecture.engines.myengine;
    ```
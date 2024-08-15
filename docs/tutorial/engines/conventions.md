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

## File structure conventions

- **Engine Files and folders**: Named in lowercase using `snake_case` format.
- **File extension**: Files with overview, environment, and dynamics content
  must end with the `.juvix.md` extension. These files must be written in
  [[Add Juvix code for specification|Juvix Markdown and include Juvix code
  blocks]] starting with a top-level module declaration. However, there is no need to
  include Juvix code if it's not necessary, but the module declaration is
  required.

- **File naming prefix**: The engine family's name is used as a prefix for all
  files related to the engine family in use. For example, the `Ticker` engine
  family would have the following files, all prefixed with `ticker_`:

    - `ticker_overview.md`
    - `ticker_environment.juvix.md`
    - `ticker_dynamics.juvix.md`
    - `ticker_protocol_types.juvix.md`
    - `ticker.juvix`

### Directory Structure

The files listed above must be organised as in the following tree view:

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
following imports.

```juvix
module node_architecture.engines.myengine;
import node_architecture.engines.myengine_environment open public;
import node_architecture.engines.myengine_dynamics open public;
import node_architecture.engines.myengine_protocol_types open public;
```

So next time, you want to use the `myengine` engine family, you can import it
using the following code:

```
import node_architecture.engines.myengine open;
```

!!! note

    To ensure new Juvix files are checked always, you also must add this module to the
    `docs/everything.juvix.md` file in the "Engines" section:

    ```diff
    module everything;

    {- Engines -}
    +import node_architecture.engines.myengine;
    ```
---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engines
- conventions
---

# Conventions for Writing Engine Families in Juvix

## Naming

<div class="annotate" markdown>

- **Engine files and folders**: Named in lowercase using `snake_case` format.

- **File extension**: Files with overview, environment, and dynamics content
  must end with the `.juvix.md` extension. These files must be written in
  [[Add Juvix code for specification|Juvix Markdown and include Juvix code blocks]]. (1)

- **File naming prefix**: The engine family's name is used as a prefix for all
  files related to the engine family in use. For example, the `Ticker` engine
  family would have the following files, all prefixed with `ticker`:

    - `ticker_overview.juvix.md`
    - `ticker_environment.juvix.md`
    - `ticker_dynamics.juvix.md`
    - `ticker_protocol_types.juvix.md`
    - `ticker.juvix`

</div>


1. Each file must have one code block at least, one declaring the Juvix module.
  For example if the file is `ticker_overview.juvix.md`, it must have the
  following code block:

    ```
    module node_architecture.engines.ticker_overview;
    ```

## File structure within the `engines` directory

The files as listed above must be stored in the `engines` directory of the
`node_architecture` directory. For example, the `ticker` engine family would
have the following directory structure:

```plaintext
node_architecture/
└── ...
└── engines/
    ├── ...
    ├── ticker_overview.md
    ├── ticker_environment.juvix.md
    ├── ticker_dynamics.juvix.md
    └── ticker_protocol_types.juvix.md
...
└── ticker.juvix
```

As you can see, the `ticker.juvix` file is not in the `engines` directory but in
the `node_architecture` directory. This file is intended to list/index all the
related files of the engine family. For example, the `ticker.juvix` file look
like this:

--8<-- "node_architecture/engines/ticker.juvix"


So next time, you want to use the `ticker` engine family, you can import it
using the following code:

```
import node_architecture.engines.ticker open;
```

As final requirement, you must add the engine family to the
`docs/everything.juvix.md` file in the "Engines" section. That is,
if the engine family is the `ticker`, you would add the following line to the file, for example

```diff
module everything;

{- Engines -}
+import node_architecture.engines.myengine;
```
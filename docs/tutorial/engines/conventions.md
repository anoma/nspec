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

- **File extension**: In case of Juvix files, the extension is `.juvix.md`. Most
likely, the file with the overview content will be `.md` file, and the rest,
that is, environment, dynamics, and protocol types, will be `.juvix.md`. These
files must be written in
[[Add Juvix code for specification|Juvix Markdown and include Juvix code blocks]].

- **File naming prefix**: The engine family's name is used as a prefix for all
  files related to the engine family in use. For example, the `Ticker` engine
  family would have the following files, all prefixed with `ticker`:

    - `ticker_overview.md`
    - `ticker_environment.juvix.md`
    - `ticker_dynamics.juvix.md`
    - `ticker_protocol_types.juvix.md`
    - `ticker.juvix`

</div>

!!! note


1. Juvix (Markdown) files have always to define the corresponding module at the
  first code block. See the [[Add Juvix code for
  specification#Juvix-Markdown-file-structure|Juvix Markdown and include Juvix
  code blocks's tutorial]]. For example if the file is
  `ticker_overview.juvix.md`, it must have the following code block:

    ```juvix
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

```
--8<-- "node_architecture/engines/ticker.juvix"
```

So next time, if you want to use the `ticker` engine family, then you can import it
using line at the top of the Juvix file:

```
import node_architecture.engines.ticker open;
```

As final requirement, you must add the engine family to the
`docs/everything.juvix.md` file in the "Engines" section. That is,
if the engine family is the `ticker`, you would add the following line:

```diff
module everything;

{- Engines -}
+import node_architecture.engines.myengine;
```
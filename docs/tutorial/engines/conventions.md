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

- **File extension**: Files must be written in Juvix Markdown, that is, the file
  must end with the extension `.juvix.md`. See [[Add Juvix code for specification|Juvix Markdown and include Juvix code blocks]].

- **File naming prefix**: The engine family's name is used as a prefix for all
  files related to the engine family in use. For example, [[Ticker Engine Overview|the `Ticker` engine family]] 
  would have the following files, all prefixed with `ticker`:

      - `ticker_overview.juvix.md`
      - `ticker_environment.juvix.md`
      - `ticker_dynamics.juvix.md`
      - `ticker.juvix`

</div>

!!! warning

    Juvix Markdownm files have always need to define the corresponding module at the
    first Juvix code block. See the [[Add Juvix code for specification#Juvix-Markdown-file-structure|Juvix Markdown and include Juvix code blocks's tutorial]]. For example if the file is
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
    ├── ticker_overview.juvix.md
    ├── ticker_environment.juvix.md
    ├── ticker_dynamics.juvix.md
    └── ticker.juvix
```

The `ticker.juvix` file is intended to list/index all the related files of the
engine family. For example, the `ticker.juvix` file look like this:

```
--8<-- "node_architecture/engines/ticker.juvix"
```

So next time, if you want to use the `ticker` engine family, then you can import it
using line at the top of the Juvix file:

```
import node_architecture.engines.ticker open;
```

## Adding the engine family to the Juvix indexes files

### To the `everything.juvix.md` file

As final requirement, you must add the engine family to the
`docs/everything.juvix.md` file in the "Engines" section. That is,
if the engine family is the `ticker`, you would add the following line:

```diff
module everything;

{- Engines -}
+import node_architecture.engines.ticker;
```

### To the `node_architecture/types/anoma_engine.juvix.md` file

```diff
module node_architecture.engines.types.anoma_engine;
import node_architecture.basics open;
...
+ import tutorial.engines.ticker as Ticker open using {Ticker};
...
type AnomaEngineFamilyType :=
...
+  | Ticker
```

### To the `node_architecture/types/anoma_message.juvix` file

```diff
...
    module node_architecture.types.anoma_message;
+      import node_architecture.engines.ticker_overview open;

type AnomaMessage :=
+  | TickerMsg Ticker.Msg
```

### To the `node_architecture/types/anoma_environment.juvix` file

```diff
...
    module node_architecture.types.anoma_environment;
+      import node_architecture.engines.ticker_environment open using {TickerEnvironment};
...
type AnomaEnvironment :=
+  | TickerEnv TickerEnvironment
```

### To the `node_architecture/types/anoma_dynamics.juvix` file

```diff
    module node_architecture.types.anoma_dynamics;
+     import node_architecture.engines.ticker_dynamics open using {TickerDynamics};
...
type AnomaDynamics :=
...
+  | TickerDynamics TickerDynamics
```

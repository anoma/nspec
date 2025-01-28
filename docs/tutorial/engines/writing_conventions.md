---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engines
- conventions
---

# Engine Writing Conventions

## Naming

<div class="annotate" markdown>

- **Engine files and folders**: Named in lowercase using `snake_case` format. See [[File naming conventions]].

- **File extension**: Files must be written in Juvix Markdown when applicable, that is, the file
  must end with the extension `.juvix.md`. See [[Add Juvix code for specification|Juvix Markdown and include Juvix code blocks]].

- **File naming prefix**: The engine's name is used as a prefix for all
  files related to the engine in use. For example, the [[Ticker Engine]]
  would have the following files, all prefixed with `ticker`:

  - `ticker.juvix.md`
  - `ticker_messages.juvix.md`
  - `ticker_config.juvix.md`
  - `ticker_environment.juvix.md`
  - `ticker_behaviour.juvix.md`

</div>

!!! warning

    Juvix Markdownm files have always need to define the corresponding module at the
    first Juvix code block. See the [[Add Juvix code for specification#Juvix-Markdown-file-structure|Juvix Markdown and include Juvix code blocks's tutorial]]. For example if the file is
    `ticker.juvix.md`, it must have the following code block:

      ```juvix
      module arch.node.engines.ticker;
      ```

## File structure within the `engines` directory

The files as listed above must be stored in the `engines` directory of the
`docs/arch/node` directory. For example, the `ticker` engine would
have the following directory structure:

```plaintext
docs/arch/node/
└── ...
└── engines/
    ├── ...
    ├── ticker.juvix.md
    ├── ticker_messages.juvix.md
    ├── ticker_config.juvix.md
    ├── ticker_environment.juvix.md
    └── ticker_behaviour.juvix.md
```

The `ticker.juvix.md` file then would contain a brief overview and list of all
its components. Check out [[Ticker Engine]] as an example for the expected
structure.

So next time, if you want to use the `ticker` engine, then you can import the
`arch.node.engines.ticker` module, adding only one line at the top of the Juvix
file where the imports are declared:

```diff
...
+ import arch.node.engines.ticker open;
```


## Update indexes

As part of defining an engine type, you must update a few files that act as indexes.

### Juvix *Everything* Index

Add import statements of all the modules related to the new engine to the
`docs/everything.juvix.md` file. The new lines must be added in the "Engines"
section. That is, if the engine is the `ticker`, we expect the following lines:

```diff title="docs/everything.juvix.md"
module everything;
...
{- Engines -}
+ import arch.node.engines.ticker;
+ import arch.node.engines.ticker_messages;
+ import arch.node.engines.ticker_config;
+ import arch.node.engines.ticker_environment;
+ import arch.node.engines.ticker_behaviour;
```


### Anoma Message

All message types must be added to the `arch/node/types/anoma_message.juvix.md` file.
Use the same pattern as the existing message types.
For example, if the engine is the `ticker`, the new type constructor should be `MsgTicker`
along with the corresponding type for the messages, that is, `TickerMsg`.

```diff title="arch/node/types/anoma_message.juvix.md"
...
module arch.node.types.anoma_message;
+ import arch.node.engines.ticker_messages open;

type Msg :=
+  | MsgTicker TickerMsg
```


### Anoma Configuration Index

All configuration types must be added to the `arch/node/types/anoma_config.juvix.md` file.
Similarly to the message types, the new type constructor should be `CfgTicker`
along with the corresponding type for the configuration, that is, `TickerCfg`.
Do not forget to import the environment type in the `Env` type.

```diff title="arch/node/types/anoma_config.juvix.md"
module arch.node.types.anoma_config;
...
+ import arch.node.engines.ticker_config open;
...
type Cfg :=
+  | CfgTicker TickerCfg
```


### Anoma Environment Index

All environment types must be added to the `arch/node/types/anoma_environment.juvix.md` file.
Similarly to the message types, the new type constructor should be `EnvTicker`
along with the corresponding type for the environment, that is, `TickerEnv`.
Do not forget to import the environment type in the `Env` type.

```diff title="arch/node/types/anoma_environment.juvix.md"
module arch.node.types.anoma_environment;
...
+ import arch.node.engines.ticker_environment open;
...
type Env :=
+  | EnvTicker TickerEnv
```

### Update the Table of Contents

Locate the navigation section in the `mkdocs.yml` file, `nav` section, and include
the new engine

```diff title="mkdocs.yml"
...
nav:
  - Protocol Architecture:
    - Node Architecture:
       ...
       - X Subsystem:
+         - Ticker Engine:
+           - Ticker Engine: ./arch/node/engines/ticker.juvix.md
+           - Ticker Messages: ./arch/node/engines/ticker_messages.juvix.md
+           - Ticker Configuration: ./arch/node/engines/ticker_config.juvix.md
+           - Ticker Environment: ./arch/node/engines/ticker_environment.juvix.md
+           - Ticker Behaviour: ./arch/node/engines/ticker_behaviour.juvix.md
```


## Using the Template engine as a starting point

The [[Template Engine]] can be used as a starting point for writing new engines.

To use it, run the following command:

```bash
nspec new engine
```

This will prompt some questions and create a new engine with the name provided
by the user and update the indexes along with the corresponding files, based on
the minimal template.

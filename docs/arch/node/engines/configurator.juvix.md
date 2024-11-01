---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.node.engines.configurator;
```

# Configuration Engine

## General Philosophy

This engine is responsible for keeping track of the settings in the
user's configuration file. The general purpose is to read the user's
configuration once and cache the information within.

## User Configuration Format

The configuration format is a
[TOML](https://en.wikipedia.org/wiki/TOML) file with the exact fields
left up to the implementation. However, there should be a field that
the user specifies where any state snapshotting happens

Below is an example of a valid configuration file.

```toml
[dump]
dump = 'anoma_iex.dmp'
[node]
name = 'anoma'
```

## Initialization

The engine just records information on the contents of the user's
configuration.

## State

```elixir
typedstruct do
  field(:configuration, Configuration.configuration_map(), enforce: true)
  field(:logger, Router.Addr.t(), enforce: false)
end
```
## Public API

```elixir
@spec snapshot(Router.addr()) :: :ok
```

The snapshot method is responsible for saving the current state of all
current machines and persisting it to the configured dump location.

```elixir
@spec delete_dump(Router.addr()) :: :ok
```

Deleting the dump is a convenience for deleting the persisted
dump. This is useful for when state updates may be incompatible, or if
the user wishes to restart all state to the genesis state.

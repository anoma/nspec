---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Engine
- Environment
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.engine_environment;

    import arch.node.types.basics open public;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Engine environment type

The engine environment encompasses static information for engine
instances in the following categories:

- A global reference, `name`, for the engine instance.
- Local state whose type is specific to the engine.
- Mailbox cluster, which is a map of mailbox IDs to mailboxes.
- A set of names of acquainted engine instances. It is implicit that the engine
  instance is acquainted with itself, so there is no need to include its own
  name.
- A list of timers that have been set.

This data is encapsulated within the `EngineEnv` type, which is
parameterised by four types:

- `S`, representing the local state,
- `M`, representing the type of mailboxes' states, and
- `H`, representing the type of handles for timers.

These same letters will be used in the rest of the document to represent these
types.

```juvix
type EngineEnv (S M H : Type) :=
  mkEngineEnv {
      localState : S;
      mailboxCluster : Map MailboxID (Mailbox M);
      acquaintances : Set EngineName;
      timers : List (Timer H);
};
```

??? info "On the mailbox cluster"

    The mailbox cluster is a map of mailbox IDs to mailboxes. The mailbox ID is
    an index type, and the mailbox is a record containing the following data:

    - The enveloped messages that the mailbox contains.
    - The mailbox state, which is of type `Option M`, i.e., it could be
    _none_.

    If you don't need multiple mailboxes, you can use any ID as the key.
    For example, you can use `0` for a default mailbox.

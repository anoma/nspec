---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Engine-Family
- Engine-Instances
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.engine_environment;
    import node_architecture.basics open;
    import node_architecture.identity_types open;
    import node_architecture.types.anoma_message as Anoma;
    ```

# Engine family environment type

The engine family environment encompasses static information for engine
instances in the following categories:

- A global reference, `name`, for the engine instance.
- Local state whose type is specific to the engine family.
- Mailbox cluster, which is a map of mailbox IDs to mailboxes.
- A set of names of acquainted engine instances. It is implicit that the engine
  instance is acquainted with itself, so there is no need to include its own
  name.
- A list of timers that have been set.

This data is encapsulated within the `EngineEnvironment` type family, which is
parameterised by four types:

- `S`, representing the local state,
- `I`, representing the type of engine-specific messages (defined in their
respective overview page),
- `M`, representing the type of mailboxes' states, and
- `H`, representing the type of handles for timers.

These same letters will be used in the rest of the document to represent these
types.

```juvix
type EngineEnvironment (S M H : Type) :=
  mkEngineEnvironment {
      name : Name ; -- read-only
      localState : S;
      mailboxCluster : Map MailboxID (Mailbox M);
      acquaintances : Set Name;
      timers : List (Timer H);
};
```

??? info "On the mailbox cluster"

    The mailbox cluster is a map of mailbox IDs to mailboxes. The mailbox ID is
    an index type, and the mailbox is a record containing the following data:

    - The enveloped messages that the mailbox contains.
    - The mailbox state, which is of type `Maybe M`, i.e., it could be
    _nothing_.

    If you don't need multiple mailboxes, you can use any ID as the key.
    For example, you can use `0` for a default mailbox.

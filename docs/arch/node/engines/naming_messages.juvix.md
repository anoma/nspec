---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - naming
  - message-types
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.naming_messages;
    import prelude open;
    import arch.node.types.identities open;
    ```

# Naming Messages

## Message interface

--8<-- "./naming_messages.juvix.md:NamingMsg"

## Message sequence diagrams

### Resolving a name

<!-- --8<-- [start:message-sequence-diagram-name-resolution] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant NamingEngine

    Client->>NamingEngine: RequestResolveName (name)
    Note over NamingEngine: Check stored evidence
    NamingEngine->>Client: ReplyResolveName
```

<figcaption markdown="span">
Resolving a name
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-name-resolution] -->

### Submitting name evidence

<!-- --8<-- [start:message-sequence-diagram-submit] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant NamingEngine

    Client->>NamingEngine: RequestSubmitNameEvidence
    Note over NamingEngine: Verify and store evidence
    NamingEngine->>Client: ReplySubmitNameEvidence
```

<figcaption markdown="span">
Submitting name evidence
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-submit] -->

### Querying name evidence

<!-- --8<-- [start:message-sequence-diagram-query] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant NamingEngine

    Client->>NamingEngine: RequestQueryNameEvidence (for ExternalIdentity)
    Note over NamingEngine: Retrieve relevant evidence
    NamingEngine->>Client: ReplyQueryNameEvidence
```

<figcaption markdown="span">
Querying name evidence for an identity.
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query] -->

## Message types

### `RequestResolveName`

```juvix
type RequestResolveName := mkRequestResolveName {
  identityName : IdentityName
};
```

A `RequestResolveName` asks the Naming Engine which `ExternalIdentity`s are
associated with a given `IdentityName`.

???+ code "Arguments"
    `identityName`:
    : The name to resolve.

### `ReplyResolveName`

```juvix
type ReplyResolveName := mkReplyResolveName {
  externalIdentities : Set ExternalIdentity;
  err : Option String
};
```

A `ReplyResolveName` is returned in response to a `RequestResolveName`.

???+ code "Arguments"

    `externalIdentities`:
    : A set of `ExternalIdentity`s associated with the `IdentityName`.

    `err`:
    : An error message if the resolution failed.

### `RequestSubmitNameEvidence`

```juvix
type RequestSubmitNameEvidence := mkRequestSubmitNameEvidence {
  evidence : IdentityNameEvidence
};
```

A `RequestSubmitNameEvidence` instructs the Naming Engine to store a new piece
of `IdentityNameEvidence`.

???+ code "Arguments"

    `evidence`:
    : The evidence supporting the association between an `IdentityName` and an `ExternalIdentity`.

### `ReplySubmitNameEvidence`

```juvix
type ReplySubmitNameEvidence := mkReplySubmitNameEvidence {
  err : Option String
};
```

A `ReplySubmitNameEvidence` is sent in response to a `RequestSubmitNameEvidence`.

???+ code "Arguments"
    `err`:
    : An error message if the submission failed.

### `RequestQueryNameEvidence`

```juvix
type RequestQueryNameEvidence := mkRequestQueryNameEvidence {
  externalIdentity : ExternalIdentity
};
```

A `RequestQueryNameEvidence` instructs the Naming Engine to return any known
`IdentityName`s and `IdentityNameEvidence` associated with a specific
`ExternalIdentity`.

???+ code "Arguments"
    `externalIdentity`:
    : The identity for which to retrieve evidence.

### `ReplyQueryNameEvidence`

```juvix
type ReplyQueryNameEvidence := mkReplyQueryNameEvidence {
  externalIdentity : ExternalIdentity;
  evidence : Set IdentityNameEvidence;
  err : Option String
};
```

A `ReplyQueryNameEvidence` provides the requested evidence.

???+ code "Arguments"

    `externalIdentity`:
    : The `ExternalIdentity` associated with the returned evidence.

    `evidence`:
    : A set of `IdentityNameEvidence` related to the identity.

    `err`:
    : An error message if the query failed.

### `NamingMsg`

<!-- --8<-- [start:NamingMsg] -->
```juvix
type NamingMsg :=
  | MsgNamingResolveNameRequest RequestResolveName
  | MsgNamingResolveNameReply ReplyResolveName
  | MsgNamingSubmitNameEvidenceRequest RequestSubmitNameEvidence
  | MsgNamingSubmitNameEvidenceReply ReplySubmitNameEvidence
  | MsgNamingQueryNameEvidenceRequest RequestQueryNameEvidence
  | MsgNamingQueryNameEvidenceReply ReplyQueryNameEvidence
  ;
```
<!-- --8<-- [end:NamingMsg] -->

## Engine components

- [[Naming Configuration]]
- [[Naming Environment]]
- [[Naming Behaviour]]
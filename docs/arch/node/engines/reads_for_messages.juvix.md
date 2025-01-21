---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-behaviour
tags:
- reads_for
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for_messages;
    import prelude open;
    import arch.node.types.identities open;
    ```

# ReadsFor Messages

## Message interface

--8<-- "./reads_for_messages.juvix.md:ReadsForMsg"

## Message sequence diagrams

### Submitting `reads_for` evidence

<!-- --8<-- [start:message-sequence-diagram-submit] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant ReadsForEngine

    Client->>ReadsForEngine: RequestSubmitReadsForEvidence
    Note over ReadsForEngine: Verify and store evidence
    ReadsForEngine->>Client: ResponseSubmitReadsForEvidence
```

<figcaption markdown="span">
Submitting `reads_for` evidence
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-submit] -->

### Querying a `reads_for` relationship

<!-- --8<-- [start:message-sequence-diagram-query-relationship] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant ReadsForEngine

    Client->>ReadsForEngine: RequestReadsFor (A reads for B?)
    Note over ReadsForEngine: Check stored evidence
    ReadsForEngine->>Client: ResponseReadsFor
```

<figcaption markdown="span">
Querying a reads_for relationship
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query-relationship] -->

  ### Querying `reads_for` evidence

<!-- --8<-- [start:message-sequence-diagram-query-evidence] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant ReadsForEngine

    Client->>ReadsForEngine: RequestQueryReadsForEvidence (for X)
    Note over ReadsForEngine: Retrieve relevant evidence
    ReadsForEngine->>Client: ResponseQueryReadsForEvidence
```

<figcaption markdown="span">
Querying reads_for evidence for an identity
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query-evidence] -->

## Message types

### `RequestReadsFor`

```juvix
type RequestReadsFor := mkRequestReadsFor {
  externalIdentityA : ExternalIdentity;
  externalIdentityB : ExternalIdentity
};
```

A request to query whether `externalIdentityA` can read data encrypted to
`externalIdentityB`.

???+ quote "Arguments"

    `externalIdentityA`:
    : The identity doing the reading.

    `externalIdentityB`:
    : The identity being read for.

### `ResponseReadsFor`

```juvix
type ResponseReadsFor := mkResponseReadsFor {
  readsFor : Bool;
  err : Option String
};
```

Response indicating whether the `reads_for` relationship exists.

???+ quote "Arguments"

    `readsFor`:
    : True if `externalIdentityA` can read for `externalIdentityB`, False otherwise.

    `err`:
    : An error message if the query failed.

### `RequestSubmitReadsForEvidence`

```juvix
type RequestSubmitReadsForEvidence := mkRequestSubmitReadsForEvidence {
  evidence : ReadsForEvidence
};
```

Request to submit evidence of a `reads_for` relationship.

???+ quote "Arguments"

    `evidence`:
    : The evidence supporting the `reads_for` relationship.

### `ResponseSubmitReadsForEvidence`

```juvix
type ResponseSubmitReadsForEvidence := mkResponseSubmitReadsForEvidence {
  err : Option String
};
```

Response acknowledging the submission of evidence.

???+ quote "Arguments"

    `err`:
    : An error message if the submission failed.

### `RequestQueryReadsForEvidence`

```juvix
type RequestQueryReadsForEvidence := mkRequestQueryReadsForEvidence {
  externalIdentity : ExternalIdentity
};
```

Request to query all `reads_for` evidence related to an identity.

???+ quote "Arguments"

    `externalIdentity`:
    : The identity for which to retrieve evidence.

### `ResponseQueryReadsForEvidence`

```juvix
type ResponseQueryReadsForEvidence := mkResponseQueryReadsForEvidence {
  externalIdentity : ExternalIdentity;
  evidence : Set ReadsForEvidence;
  err : Option String
};
```

Response providing the requested evidence.

???+ quote "Arguments"

    `externalIdentity`:
    : The identity for which evidence was requested.

    `evidence`:
    : A set of `ReadsForEvidence` related to the identity.

    `err`:
    : An error message if the query failed.

### `ReadsForMsg`

<!-- --8<-- [start:ReadsForMsg] -->
```juvix
type ReadsForMsg :=
  | MsgReadsForRequest RequestReadsFor
  | MsgReadsForResponse ResponseReadsFor
  | MsgSubmitReadsForEvidenceRequest RequestSubmitReadsForEvidence
  | MsgSubmitReadsForEvidenceResponse ResponseSubmitReadsForEvidence
  | MsgQueryReadsForEvidenceRequest RequestQueryReadsForEvidence
  | MsgQueryReadsForEvidenceResponse ResponseQueryReadsForEvidence
  ;
```
<!-- --8<-- [start:ReadsForMsg] -->

## Engine Components

- [[ReadsFor Configuration]]
- [[ReadsFor Environment]]
- [[ReadsFor Behaviour]]

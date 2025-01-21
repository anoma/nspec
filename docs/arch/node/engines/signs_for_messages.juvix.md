---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-behaviour
tags:
- signs_for
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for_messages;
    import prelude open;
    import arch.node.types.identities open;
    ```

# SignsFor Messages

## Message interface

--8<-- "./signs_for_messages.juvix:SignsForMsg"

## Message sequence diagrams

### Submitting `signs_for` evidence

<!-- --8<-- [start:message-sequence-diagram-submit] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant SignsForEngine

    Client->>SignsForEngine: RequestSubmitSignsForEvidence
    Note over SignsForEngine: Process and store evidence
    SignsForEngine->>Client: ResponseSubmitSignsForEvidence
```

<figcaption markdown="span">
Submitting evidence of a signs_for relationship
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-submit] -->

### Querying `signs_for` relationship

<!-- --8<-- [start:message-sequence-diagram-query-relation] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant SignsForEngine

    Client->>SignsForEngine: RequestSignsFor (X signs for Y?)
    Note over SignsForEngine: Check stored evidence
    SignsForEngine->>Client: ResponseSignsFor
```

<figcaption markdown="span">
Querying whether a specific signs_for relationship exists
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query-relation] -->

### Retrieving `signs_for` evidence

<!-- --8<-- [start:message-sequence-diagram-query-evidence] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant SignsForEngine

    Client->>SignsForEngine: RequestQuerySignsForEvidence (for X)
    Note over SignsForEngine: Retrieve relevant evidence
    SignsForEngine->>Client: ResponseQuerySignsForEvidence
```

<figcaption markdown="span">
Retrieving all signs_for evidence related to a particular identity
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query-evidence] -->

## Message types

### `RequestSignsFor`

```juvix
type RequestSignsFor := mkRequestSignsFor {
  externalIdentityA : ExternalIdentity;
  externalIdentityB : ExternalIdentity
};
```

A `RequestSignsFor` queries whether `externalIdentityA` can sign on behalf of
`externalIdentityB`.

???+ quote "Arguments"

    `externalIdentityA`:
    : The identity attempting to sign.

    `externalIdentityB`:
    : The identity on whose behalf the signature is made.

### `MsgSignsForResponse ResponseSignsFor`

```juvix
type ResponseSignsFor := mkResponseSignsFor {
  signsFor : Bool;
  err : Option String
};
```

A `ResponseSignsFor` indicates whether the `signs_for` relationship exists.

???+ quote "Arguments"

    `signsFor`:
    : True if `externalIdentityA` can sign for `externalIdentityB`, False otherwise.

    `err`:
    : An error message if the query failed.

### `RequestSubmitSignsForEvidence`

```juvix
type RequestSubmitSignsForEvidence := mkRequestSubmitSignsForEvidence {
  evidence : SignsForEvidence
};
```

A `RequestSubmitSignsForEvidence` submits evidence of a `signs_for` relationship.

???+ quote "Arguments"
    `evidence`:
    : The evidence supporting the `signs_for` relationship.

### `ResponseSubmitSignsForEvidence`

```juvix
type ResponseSubmitSignsForEvidence := mkResponseSubmitSignsForEvidence {
  err : Option String
};
```

A `ResponseSubmitSignsForEvidence` acknowledges the submission of evidence.

???+ quote "Arguments"
    `err`:
    : An error message if the submission failed.

### `RequestQuerySignsForEvidence`

```juvix
type RequestQuerySignsForEvidence := mkRequestQuerySignsForEvidence {
  externalIdentity : ExternalIdentity
};
```

A `RequestQuerySignsForEvidence` queries all `signs_for` evidence related to an identity.

???+ quote "Arguments"
    `externalIdentity`:
    : The identity for which to retrieve evidence.

### `ResponseQuerySignsForEvidence`

```juvix
type ResponseQuerySignsForEvidence := mkResponseQuerySignsForEvidence {
  externalIdentity : ExternalIdentity;
  evidence : Set SignsForEvidence;
  err : Option String
};
```

A `ResponseQuerySignsForEvidence` provides the requested evidence.

???+ quote "Arguments"

    `externalIdentity`:
    : The identity for which to retrieve evidence.

    `evidence`:
    : A set of `SignsForEvidence` related to the identity.

    `err`:
    : An error message if the query failed.

### `SignsForMsg`

<!-- --8<-- [start:SignsForMsg] -->
```juvix
type SignsForMsg :=
  | MsgSignsForRequest RequestSignsFor
  | MsgSignsForResponse ResponseSignsFor
  | MsgSubmitSignsForEvidenceRequest RequestSubmitSignsForEvidence
  | MsgSubmitSignsForEvidenceResponse ResponseSubmitSignsForEvidence
  | MsgQuerySignsForEvidenceRequest RequestQuerySignsForEvidence
  | MsgQuerySignsForEvidenceResponse ResponseQuerySignsForEvidence
  ;
```
<!-- --8<-- [end:SignsForMsg] -->

## Engine Components

- [[SignsFor Configuration]]
- [[SignsFor Environment]]
- [[SignsFor Behaviour]]

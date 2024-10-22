---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
tags:
- signs_for
- engine-overview
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.signs_for_overview;
    import prelude open;
    import node_architecture.types.identities open;
    import node_architecture.identity_types open;
    ```

# `Signs For` Engine Family Overview

--8<-- "./docs/node_architecture/engines/signs_for.juvix.md:signs-for-engine-family"

The Signs For Engine manages `signs_for` relationships between identities. A `signs_for` relationship indicates that one identity can produce signatures (commitments) on behalf of another identity.

## Purpose

The Signs For Engine maintains and manages the state of `signs_for` relationships between identities. It handles queries about these relationships, allows submission of new evidence, and provides information about existing relationships. This is useful in scenarios where signature delegation or proxy signing is required.

## Message interface

<!-- --8<-- [start:SignsForMsg] -->
```juvix
type SignsForMsg :=
  | -- --8<-- [start:SignsForRequest]
    SignsForRequest {
      externalIdentityA : ExternalIdentity;
      externalIdentityB : ExternalIdentity
    }
    -- --8<-- [end:SignsForRequest]
  | -- --8<-- [start:SignsForResponse]
    SignsForResponse {
      signsFor : Bool;
      err : Option String
    }
    -- --8<-- [end:SignsForResponse]
  | -- --8<-- [start:SubmitSignsForEvidenceRequest]
    SubmitSignsForEvidenceRequest {
      evidence : SignsForEvidence
    }
    -- --8<-- [end:SubmitSignsForEvidenceRequest]
  | -- --8<-- [start:SubmitSignsForEvidenceResponse]
    SubmitSignsForEvidenceResponse {
      err : Option String
    }
    -- --8<-- [end:SubmitSignsForEvidenceResponse]
  | -- --8<-- [start:QuerySignsForEvidenceRequest]
    QuerySignsForEvidenceRequest {
      externalIdentity : ExternalIdentity
    }
    -- --8<-- [end:QuerySignsForEvidenceRequest]
  | -- --8<-- [start:QuerySignsForEvidenceResponse]
    QuerySignsForEvidenceResponse {
      externalIdentity : ExternalIdentity;
      evidence : Set SignsForEvidence;
      err : Option String
    }
    -- --8<-- [end:QuerySignsForEvidenceResponse]
  ;
```
<!-- --8<-- [end:SignsForMsg] -->

### `SignsForRequest` message

!!! quote "SignsForRequest"

    ```
    --8<-- "./signs_for_overview.juvix.md:SignsForRequest"
    ```

A `SignsForRequest` queries whether `externalIdentityA` can sign on behalf of `externalIdentityB`.

- `externalIdentityA`: The identity attempting to sign.
- `externalIdentityB`: The identity on whose behalf the signature is made.

### `SignsForResponse` message

!!! quote "SignsForResponse"

    ```
    --8<-- "./signs_for_overview.juvix.md:SignsForResponse"
    ```

A `SignsForResponse` indicates whether the `signs_for` relationship exists.

- `signsFor`: True if externalIdentityA can sign for externalIdentityB, False otherwise.
- `err`: An error message if the query failed.

### `SubmitSignsForEvidenceRequest` message

!!! quote "SubmitSignsForEvidenceRequest"

    ```
    --8<-- "./signs_for_overview.juvix.md:SubmitSignsForEvidenceRequest"
    ```

A `SubmitSignsForEvidenceRequest` submits evidence of a `signs_for` relationship.

- `evidence`: The evidence supporting the `signs_for` relationship.

### `SubmitSignsForEvidenceResponse` message

!!! quote "SubmitSignsForEvidenceResponse"

    ```
    --8<-- "./signs_for_overview.juvix.md:SubmitSignsForEvidenceResponse"
    ```

A `SubmitSignsForEvidenceResponse` acknowledges the submission of evidence.

- `err`: An error message if the submission failed.

### `QuerySignsForEvidenceRequest` message

!!! quote "QuerySignsForEvidenceRequest"

    ```
    --8<-- "./signs_for_overview.juvix.md:QuerySignsForEvidenceRequest"
    ```

A `QuerySignsForEvidenceRequest` queries all `signs_for` evidence related to an identity.

- `externalIdentity`: The identity for which to retrieve evidence.

### `QuerySignsForEvidenceResponse` message

!!! quote "QuerySignsForEvidenceResponse"

    ```
    --8<-- "./signs_for_overview.juvix.md:QuerySignsForEvidenceResponse"
    ```

A `QuerySignsForEvidenceResponse` provides the requested evidence.

- `evidence`: A set of SignsForEvidence related to the identity.
- `err`: An error message if the query failed.

## Message sequence diagrams

### Submitting Signs For Evidence

<!-- --8<-- [start:message-sequence-diagram-submit] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant SignsForEngine

    Client->>SignsForEngine: SubmitSignsForEvidenceRequest
    Note over SignsForEngine: Process and store evidence
    SignsForEngine->>Client: SubmitSignsForEvidenceResponse
```

<figcaption markdown="span">
Submitting evidence of a signs_for relationship
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-submit] -->

### Querying Signs For Relationship

<!-- --8<-- [start:message-sequence-diagram-query-relation] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant SignsForEngine

    Client->>SignsForEngine: SignsForRequest (X signs for Y?)
    Note over SignsForEngine: Check stored evidence
    SignsForEngine->>Client: SignsForResponse
```

<figcaption markdown="span">
Querying whether a specific signs_for relationship exists
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query-relation] -->

### Retrieving Signs For Evidence

<!-- --8<-- [start:message-sequence-diagram-query-evidence] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant Client
    participant SignsForEngine

    Client->>SignsForEngine: QuerySignsForEvidenceRequest (for X)
    Note over SignsForEngine: Retrieve relevant evidence
    SignsForEngine->>Client: QuerySignsForEvidenceResponse
```

<figcaption markdown="span">
Retrieving all signs_for evidence related to a particular identity
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-query-evidence] -->

## Engine Components

- [[Signs For Environment|`Signs For` Engine Environment]]
- [[Signs For Dynamics|`Signs For` Engine Dynamics]]

## Useful links

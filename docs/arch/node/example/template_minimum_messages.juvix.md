---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- template_minimum-minimum-engine
- engine-messages
---

??? note "Juvix imports"

    ```juvix
    module arch.node.example.template_minimum_messages;
    import prelude open;
    ```

# TemplateMinimum Messages

These are the messages that the TemplateMinimum engine can receive/respond to.

## Message interface

### `TemplateMinimumMsgJustHi`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateMinimumMsgExampleRequest ExampleRequest`

Example request.

<!-- --8<-- [start:ExampleRequest] -->
```juvix
type ExampleRequest : Type :=
  mkExampleRequest {
    argOne : Nat;
    argTwo : Nat;
  }
```
<!-- --8<-- [end:ExampleRequest] -->

???+ quote "Arguments"

    `argOne`
    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `argTwo`
    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateMinimumMsgExampleReply ExampleReply`

Reply to an `ExampleRequest`.

#### `ExampleReplyOk`

Example OK reply.

<!-- --8<-- [start:ExampleReplyOk] -->
```juvix
type ExampleReplyOk : Type :=
  mkExampleReplyOk {
    argOne : Nat;
  }
```
<!-- --8<-- [end:ExampleReplyOk] -->

???+ quote "Arguments"

    `argOne`
    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

#### `ExampleReplyError`

Example error reply.

<!-- --8<-- [start:ExampleReplyError] -->
```juvix
type ExampleReplyError : Type :=
  | ExampleErrorOne
  | ExampleErrorTwo
  ;
```
<!-- --8<-- [end:ExampleReplyError] -->

???+ quote "Error types"

    `ExampleErrorOne`
    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    `ExampleErrorTwo`
    : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

#### `ExampleReply`

<!-- --8<-- [start:ExampleReply] -->
```juvix
ExampleReply : Type := Result ExampleReplyError ExampleReplyOk;
```
<!-- --8<-- [end:ExampleReply] -->

### `TemplateMinimumMsg`

<!-- --8<-- [start:TemplateMinimumMsg] -->
```juvix
type TemplateMinimumMsg :=
  | TemplateMinimumMsgJustHi
  | TemplateMinimumMsgExampleRequest ExampleRequest
  | TemplateMinimumMsgExampleReply ExampleReply
  ;
```
<!-- --8<-- [end:TemplateMinimumMsg] -->

## Sequence Diagrams

### `ExampleRequest` & `ExampleReply`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed ut purus eget sapien. Nulla facilisi.

<!-- --8<-- [start:message-sequence-diagram-ExampleRequest] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant TemplateMinimumClient
    participant TemplateMinimum

    TemplateMinimumClient ->> TemplateMinimum: ExampleRequest
    TemplateMinimum ->> TemplateMinimumClient: ExampleReplyOk

    TemplateMinimumClient ->> TemplateMinimum: ExampleRequest
    TemplateMinimum ->> TemplateMinimumClient: ExampleReplyErrorOne
```

<figcaption markdown="span">
Sequence Diagram: `ExampleRequest` & `ExampleReply`
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram-ExampleRequest] -->


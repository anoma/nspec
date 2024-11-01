---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# SignsForRequest

# SignsForResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `SignsForRequest` asks the signs_for engine whether one identity can signs for another.

A `SignsForResponse` is returned in response to a [[SignsForRequest]]
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
[[SignsForRequest]]
[[SignsForResponse]]
<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
- Returns a [[SignsForResponse]] according to whether A `signsFor` B, given the known evidence
<!-- --8<-- [end:behaviour] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ SignsForEngine: SignsForRequest
SignsForEngine -->>- Any Local Engine: SignsForResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

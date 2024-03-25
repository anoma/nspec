<div class="message" markdown>


# SignsForRequest
# SignsForResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `SignsForRequest` asks the signs-for engine whether one identity can signs for another.

A `SignsForResponse` is returned in response to a [[SignsForRequest]]
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
[[SignsForRequest]]
[[SignsForResponse]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
- Returns a [[SignsForResponse]] according to whether A `signsFor` B, given the known evidence
<!-- --8<-- [end:behavior] -->

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
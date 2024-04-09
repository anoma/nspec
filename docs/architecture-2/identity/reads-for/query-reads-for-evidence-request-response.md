<div class="message" markdown>

# QueryReadsForEvidenceRequest

# QueryReadsForEvidenceResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `QueryReadsForEvidenceRequest` instructs the reads-for engine to read and return the known reads-for evidence associated with a specific external identity.

A `QueryReadsForEvidenceResponse` is returned by the reads-for engine in response to a [[QueryReadsForEvidenceRequest]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
[[QueryReadsForEvidenceRequest]]
[[QueryReadsForEvidenceResponse]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
- Returns known evidence in a [[QueryReadsForEvidenceResponse]]
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ ReadsForEngine: QueryReadsForEvidenceRequest
ReadsForEngine -->>- Any Local Engine: QueryReadsForEvidenceResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

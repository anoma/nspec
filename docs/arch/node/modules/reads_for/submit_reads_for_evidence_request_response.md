---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# SubmitReadsForEvidenceRequest

# SubmitReadsForEvidenceResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `SubmitReadsForEvidenceRequest` instructs the reads_for engine to store a new piece of reads_for evidence.

A `SubmitReadsForEvidenceResponse` is sent in response to a [[SubmitReadsForEvidenceRequest]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
[[SubmitReadsForEvidenceRequest]]
[[SubmitReadsForEvidenceResponse]]
<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
Describe the message reception behaviour, processing logic, and possible triggers.
- Stores the submitted evidence
- Returns an error iff.
    - The evidence is invalid
    - The evidence was already stored
<!-- --8<-- [end:behaviour] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ ReadsForEngine: SubmitReadsForEvidenceRequest
ReadsForEngine -->>- Any Local Engine: SubmitReadsForEvidenceResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>

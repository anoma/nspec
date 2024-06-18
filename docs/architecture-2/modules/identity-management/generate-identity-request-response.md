---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# GenerateIdentityRequest

# GenerateIdentityResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `GenerateIdentityRequest` instructs the identity management engine to generate a new identity using the specified backend.

A `GenerateIdentityResponse` provides the handles to decryption and commitment engine instances for a newly generated identity, or an error if a failure occurred.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
[[GenerateIdentityRequest]]
[[GenerateIdentityResponse]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
- Uses the designated backend to generate a new identity
- Creates new commitment engine and decryption engine instances
- Returns handles to those instances in a [[GenerateIdentityResponse]]
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ IdentityManagementEngine: GenerateIdentityRequest
IdentityManagementEngine -->>- Any Local Engine: GenerateIdentityResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>
